# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Module for IoCExtract class.

Uses a set of builtin regular expressions to look for Indicator of
Compromise (IoC) patterns. Input can be a single string or a pandas
dataframe with one or more columns specified as input.

The following types are built-in:

-  IPv4 and IPv6
-  URL
-  DNS domain
-  Hashes (MD5, SHA1, SHA256)
-  Windows file paths
-  Linux file paths (this is kind of noisy because a legal linux file
   path can have almost any character) You can modify or add to the
   regular expressions used at runtime.

"""

import re
from collections import namedtuple, defaultdict
from typing import Any, List, Mapping, Set, Dict, Tuple
from urllib.parse import unquote

import pandas as pd
from .. nbtools.utility import export
from .. _version import VERSION

__version__ = VERSION
__author__ = 'Ian Hellen'


def _compile_regex(regex):
    return re.compile(regex, re.I | re.X | re.M)


IoCPattern = namedtuple('IoCPattern', ['ioc_type', 'comp_regex', 'priority', 'group'])


@export
class IoCExtract:
    """
    IoC Extractor - looks for common IoC patterns in input strings.

    The extract() method takes either a string or a pandas DataFrame
    as input. When using the string option as an input extract will
    return a dictionary of results. When using a DataFrame the results
    will be returned as a new DataFrame with the following columns:
    IoCType: the mnemonic used to distinguish different IoC Types
    Observable: the actual value of the observable
    SourceIndex: the index of the row in the input DataFrame from
    which the source for the IoC observable was extracted.

    The class has a number of built-in IoC regex definitions.
    These can be retrieved using the ioc_types attribute.

    Addition IoC definitions can be added using the add_ioc_type
    method.

    Note: due to some ambiguity in the regular expression patterns
    for different types and observable may be returned assigned to
    multiple observable types. E.g. 192.168.0.1 is a also a legal file
    name in both Linux and Windows. Linux file names have a particularly
    large scope in terms of legal characters so it will be quite common
    to see other IoC observables (or parts of them) returned as a
    possible linux path.
    """

    IPV4_REGEX = r'(?P<ipaddress>(?:[0-9]{1,3}\.){3}[0-9]{1,3})'
    IPV6_REGEX = r'(?<![:.\w])(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}(?![:.\w])'
    DNS_REGEX = r'((?=[a-z0-9-]{1,63}\.)[a-z0-9]+(-[a-z0-9]+)*\.){2,}[a-z]{2,63}'
    # dns_regex =
    #   '\\b((?=[a-z0-9-]{1,63}\\.)[a-z0-9]+(-[a-z0-9]+)*\\.){2,}[a-z]{2,63}\\b'

    URL_REGEX = r'''
            (?P<protocol>(https?|ftp|telnet|ldap|file)://)
            (?P<userinfo>([a-z0-9-._~!$&\'()*+,;=:]|%[0-9A-F]{2})*@)?
            (?P<host>([a-z0-9-._~!$&\'()*+,;=]|%[0-9A-F]{2})*)
            (:(?P<port>\d*))?
            (/(?P<path>([^?\#"<> ]|%[0-9A-F]{2})*/?))?
            (\?(?P<query>([a-z0-9-._~!$&'()*+,;=:/?@]|%[0-9A-F]{2})*))?
            (\#(?P<fragment>([a-z0-9-._~!$&'()*+,;=:/?@]|%[0-9A-F]{2})*))?'''

    WINPATH_REGEX = r'''
            (?P<root>[a-z]:|\\\\[a-z0-9_.$-]+||[.]+)
            (?P<folder>\\(?:[^\/:*?"\'<>|\r\n]+\\)*)
            (?P<file>[^\\/*?""<>|\r\n ]+)'''
    # Linux simplified - this ignores some legal linux paths avoid matching too much
    # This also matches URLs but these should be thrown out by priority
    # weighting since URL has a higher priority
    LXPATH_REGEX = r'''(?P<root>/+||[.]+)
            (?P<folder>/(?:[^\\/:*?<>|\r\n]+/)*)
            (?P<file>[^/\0<>|\r\n ]+)'''

    MD5_REGEX = r'(?:^|[^A-Fa-f0-9])(?P<hash>[A-Fa-f0-9]{32})(?:$|[^A-Fa-f0-9])'
    SHA1_REGEX = r'(?:^|[^A-Fa-f0-9])(?P<hash>[A-Fa-f0-9]{40})(?:$|[^A-Fa-f0-9])'
    SHA256_REGEX = r'(?:^|[^A-Fa-f0-9])(?P<hash>[A-Fa-f0-9]{64})(?:$|[^A-Fa-f0-9])'

    _content_regex: Dict[str, IoCPattern] = {}

    def __init__(self):
        """Intialize new instance of IoCExtract."""
        # IP Addresses
        self.add_ioc_type('ipv4', self.IPV4_REGEX, 0, 'ipaddress')
        self.add_ioc_type('ipv6', self.IPV6_REGEX, 0)

        # Dns Domains
        # This also matches IP addresses but IPs have higher
        # priority both matching on the same substring will defer
        # to the IP regex
        self.add_ioc_type('dns', self.DNS_REGEX, 1)

        # Http requests
        self.add_ioc_type('url', self.URL_REGEX, 0)

        # File paths
        # Windows
        self.add_ioc_type('windows_path', self.WINPATH_REGEX, 2)

        self.add_ioc_type('linux_path', self.LXPATH_REGEX, 2)

        # MD5, SHA1, SHA256 hashes
        self.add_ioc_type('md5_hash', self.MD5_REGEX, 1, 'hash')
        self.add_ioc_type('sha1_hash', self.SHA1_REGEX, 1, 'hash')
        self.add_ioc_type('sha256_hash', self.SHA256_REGEX, 1, 'hash')

    # Public members

    def add_ioc_type(self, ioc_type: str,
                     ioc_regex: str,
                     priority: int = 0,
                     group: str = None):
        """
        Add an IoC type and regular expression to use to the built-in set.

        Parameters
        ----------
        ioc_type : str
            A unique name for the IoC type
        ioc_regex : str
            A regular expression used to search for the type
        priority : int, optional
            Priority of the regex match vs. other ioc_patterns. 0 is
            the highest priority (the default is 0).
        group : str, optional
            The regex group to match (the default is None,
            which will match on the whole expression)

        Notes
        -----
        Pattern priorities.
            If two IocType patterns match on the same substring, the matched
            substring is assigned to the pattern/IocType with the highest
            priority. E.g. `foo.bar.com` will match types: `dns`, `windows_path`
            and `linux_path` but since `dns` has a higher priority, the expression
            is assigned to the `dns` matches.

        """
        if ioc_type is None or ioc_type.strip() is None:
            raise Exception('No value supplied for ioc_type parameter')
        if ioc_regex is None or ioc_regex.strip() is None:
            raise Exception('No value supplied for ioc_regex parameter')

        self._content_regex[ioc_type] = IoCPattern(ioc_type=ioc_type,
                                                   comp_regex=_compile_regex(
                                                       regex=ioc_regex),
                                                   priority=priority,
                                                   group=group)

    @property
    def ioc_types(self) -> dict:
        """
        Return the current set of IoC types and regular expressions.

        Returns
        -------
        dict
            dict of IoC Type names and regular expressions

        """
        return self._content_regex

# pylint: disable=too-many-locals
    def extract(self, src: str = None,
                data: pd.DataFrame = None,
                columns: List[str] = None,
                **kwargs) -> Any:
        """
        Extract IoCs from either a string or pandas DataFrame.

        Parameters
        ----------
        src : str, optional
            source string in which to look for IoC patterns
            (the default is None)
        data : pd.DataFrame, optional
            input DataFrame from which to read source strings
            (the default is None)
        columns : list, optional
            The list of columns to use as source strings,
            if the `data` parameter is used. (the default is None)

        Other Parameters
        ----------------
        os_family : str, optional
            'Linux' or 'Windows' (the default is 'Windows'). This
            is used to toggle between Windows or Linux path matching.
        ioc_types : list, optional
            Restrict matching to just specified types.
            (default is all types)
        include_paths : bool, optional
            Whether to include path matches (which can be noisy)
            (the default is false - excludes 'windows_path'
            and 'linux_path'). If `ioc_types` is specified
            this parameter is ignored.

        Returns
        -------
        Any
            dict of found observables (if input is a string) or
            DataFrame of observables

        Notes
        -----
        Extract takes either a string or a pandas DataFrame as input.
        When using the string option as an input extract will
        return a dictionary of results.
        When using a DataFrame the results will be returned as a new
        DataFrame with the following columns:
        - IoCType: the mnemonic used to distinguish different IoC Types
        - Observable: the actual value of the observable
        - SourceIndex: the index of the row in the input DataFrame from
        which the source for the IoC observable was extracted.

        IoCType Pattern selection
        The default list is:  ['ipv4', 'ipv6', 'dns', 'url',
        'md5_hash', 'sha1_hash', 'sha256_hash'] plus any
        user-defined types.
        'windows_path', 'linux_path' are excluded unless `include_paths`
        is True or explicitly included in `ioc_paths`.

        """
        os_family = kwargs.get('os_family', 'Windows')
        ioc_types = kwargs.get('ioc_types', None)
        include_paths = kwargs.get('include_paths', False)

        if src and src.strip():
            return self._scan_for_iocs(src=src, os_family=os_family,
                                       ioc_types=ioc_types)

        if data is None:
            raise Exception('No source data was supplied to extract')

        if columns is None:
            raise Exception(
                'No values were supplied for the columns parameter')

        # Use only requested IoC Type patterns
        if ioc_types:
            ioc_types_to_use = list(set(ioc_types))
        else:
            ioc_types_to_use = list(set(self._content_regex.keys()))
            if not include_paths:
                ioc_types_to_use.remove('windows_path')
                ioc_types_to_use.remove('linux_path')

        col_set = set(columns)
        if not col_set <= set(data.columns):
            missing_cols = [
                elem for elem in col_set if elem not in data.colums]
            raise Exception('Source column(s) {} not found in supplied DataFrame'
                            .format(', '.join(missing_cols)))

        result_columns = ['IoCType', 'Observable', 'SourceIndex']
        result_frame = pd.DataFrame(columns=result_columns)
        for idx, datarow in data.iterrows():
            for col in columns:
                ioc_results = self._scan_for_iocs(
                    datarow[col], os_family, ioc_types_to_use)
                for result_type, result_set in ioc_results.items():
                    if result_set:
                        for observable in result_set:
                            result_row = pd.Series(
                                data=[result_type, observable, idx],
                                index=result_columns)
                            result_frame = result_frame.append(
                                result_row, ignore_index=True)

        return result_frame

    def extract_df(self,
                   data: pd.DataFrame,
                   columns: List[str],
                   **kwargs) -> pd.DataFrame:
        """
        Extract IoCs from either a pandas DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            input DataFrame from which to read source strings
        columns : list
            The list of columns to use as source strings,

        Other Parameters
        ----------------
        os_family : str, optional
            'Linux' or 'Windows' (the default is 'Windows'). This
            is used to toggle between Windows or Linux path matching.
        ioc_types : list, optional
            Restrict matching to just specified types.
            (default is all types)
        include_paths : bool, optional
            Whether to include path matches (which can be noisy)
            (the default is false - excludes 'windows_path'
            and 'linux_path'). If `ioc_types` is specified
            this parameter is ignored.

        Returns
        -------
        pd.DataFrame
            DataFrame of observables

        Notes
        -----
        Extract takes a pandas DataFrame as input.
        The results will be returned as a new
        DataFrame with the following columns:
        - IoCType: the mnemonic used to distinguish different IoC Types
        - Observable: the actual value of the observable
        - SourceIndex: the index of the row in the input DataFrame from
        which the source for the IoC observable was extracted.

        IoCType Pattern selection
        The default list is:  ['ipv4', 'ipv6', 'dns', 'url',
        'md5_hash', 'sha1_hash', 'sha256_hash'] plus any
        user-defined types.
        'windows_path', 'linux_path' are excluded unless `include_paths`
        is True or explicitly included in `ioc_paths`.

        """
        os_family = kwargs.get('os_family', 'Windows')
        ioc_types = kwargs.get('ioc_types', None)
        include_paths = kwargs.get('include_paths', False)

        # Use only requested IoC Type patterns
        if ioc_types:
            ioc_types_to_use = list(set(ioc_types))
        else:
            ioc_types_to_use = list(set(self._content_regex.keys()))
            if not include_paths:
                ioc_types_to_use.remove('windows_path')
                ioc_types_to_use.remove('linux_path')

        col_set = set(columns)
        if not col_set <= set(data.columns):
            missing_cols = [
                elem for elem in col_set if elem not in data.colums]
            raise Exception('Source column(s) {} not found in supplied DataFrame'
                            .format(', '.join(missing_cols)))

        result_columns = ['IoCType', 'Observable', 'SourceIndex']
        result_frame = pd.DataFrame(columns=result_columns)
        for idx, datarow in data.iterrows():
            for col in columns:
                ioc_results = self._scan_for_iocs(
                    datarow[col], os_family, ioc_types_to_use)
                for result_type, result_set in ioc_results.items():
                    if result_set:
                        for observable in result_set:
                            result_row = pd.Series(
                                data=[result_type, observable, idx],
                                index=result_columns)
                            result_frame = result_frame.append(
                                result_row, ignore_index=True)

        return result_frame

    def validate(self, input_str: str, ioc_type: str) -> bool:
        """
        Check that `input_str` matches the regex for the specificed `ioc_type`.

        Parameters
        ----------
        input_str : str
            the string to test
        ioc_type : str
            the regex pattern to use

        Returns
        -------
        bool
            True if match.

        """
        if ioc_type not in self._content_regex:
            raise KeyError('Unknown type {}. Valid types are: {}'
                           .format(ioc_type, list(self._content_regex.keys())))
        rgx = self._content_regex[ioc_type]
        return rgx.comp_regex.fullmatch(input_str) is not None

    # Private methods
    def _scan_for_iocs(self, src: str,
                       os_family: str,
                       ioc_types: List[str] = None) -> Mapping[str, Set[str]]:
        """Return IoCs found in the string."""
        ioc_results: Dict[str, Set] = defaultdict(set)
        iocs_found: Dict[str, Tuple[str, int]] = {}

# pylint: disable=too-many-nested-blocks
        for (ioc_type, rgx_def) in self._content_regex.items():
            if ioc_types and ioc_type not in ioc_types:
                continue

            if os_family == 'Linux' and rgx_def.ioc_type == 'windows_path':
                continue
            elif os_family == 'Windows' and rgx_def.ioc_type == 'linux_path':
                continue

            match_pos = 0
            for rgx_match in rgx_def.comp_regex.finditer(src, match_pos):
                if rgx_match is None:
                    break
                # If the rgx_def names a group to match on, use that
                match_str = (rgx_match.groupdict()[rgx_def.group]
                             if rgx_def.group else rgx_match.group())

                self._add_highest_pri_match(iocs_found,
                                            match_str,
                                            rgx_def)
                if ioc_type == 'url':
                    decoded_url = unquote(match_str)
                    for url_match in rgx_def.comp_regex.finditer(decoded_url,
                                                                 match_pos):
                        if url_match is not None:
                            self._add_highest_pri_match(iocs_found,
                                                        url_match.group(),
                                                        rgx_def)
                            self._add_highest_pri_match(iocs_found,
                                                        url_match.groupdict()[
                                                            'host'],
                                                        self._content_regex['dns'])
                match_pos = rgx_match.end()

        for ioc, ioc_result in iocs_found.items():
            ioc_results[ioc_result[0]].add(ioc)

        return ioc_results

    @staticmethod
    def _add_highest_pri_match(iocs_found: dict,
                               current_match: str,
                               current_def: IoCPattern):
        # if we already found a match for this item and the previous
        # ioc type is more specific then don't add this to the results
        if (current_match in iocs_found
                and current_def.priority >= iocs_found[current_match][1]):
            return

        iocs_found[current_match] = (
            current_def.ioc_type, current_def.priority)
