# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016 Chris Lamb <lamby@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.

EXTERNAL_TOOLS = {
    'abootimg': {'debian': 'abootimg'},
    'apktool': {'debian': 'apktool'},
    'db_dump': {'debian': 'db-util'},
    'bsdtar': {
        'debian': 'libarchive-tools',
        'arch': 'libarchive',
        'fedora': 'bsdtar',
        'FreeBSD': 'libarchive',
    },
    'bzip2': {'debian': 'bzip2', 'arch': 'bzip2'},
    'cbfstool': {},
    'cd-iccdump': {'debian': 'colord', 'arch': 'colord', 'FreeBSD': 'colord'},
    'cmp': {'debian': 'diffutils', 'arch': 'diffutils'},
    'compare': {'debian': 'imagemagick', 'arch': 'imagemagick'},
    'cpio': {'debian': 'cpio', 'arch': 'cpio'},
    'diff': {'debian': 'diffutils', 'arch': 'diffutils'},
    'docx2txt': {'debian': 'docx2txt', 'arch': 'docx2txt'},
    'enjarify': {'debian': 'enjarify', 'arch': 'enjarify'},
    'fdtdump': {'debian': 'device-tree-compiler', 'arch': 'dtc'},
    'ffprobe': {'debian': 'ffmpeg'},
    'file': {'debian': 'file', 'arch': 'file'},
    'find': {'debian': 'findutils', 'arch': 'findutils'},
    'getfacl': {'debian': 'acl', 'arch': 'acl'},
    'gifbuild': {'debian': 'giflib-tools', 'arch': 'giflib'},
    'ghc': {'debian': 'ghc', 'arch': 'ghc', 'FreeBSD': 'ghc'},
    'gpg': {'debian': 'gnupg', 'arch': 'gnupg', 'FreeBSD': 'gnupg'},
    'gzip': {'debian': 'gzip', 'arch': 'gzip'},
    'identify': {'debian': 'imagemagick', 'arch': 'imagemagick'},
    'img2txt': {
        'debian': 'caca-utils',
        'arch': 'libcaca',
        'FreeBSD': 'libcaca',
    },
    'isoinfo': {
        'debian': 'genisoimage',
        'arch': 'cdrtools',
        'FreeBSD': 'cdrtools',
    },
    'javap': {
        'debian': 'default-jdk-headless | default-jdk | java-sdk',
        'arch': 'java-environment',
    },
    'js-beautify': {'debian': 'jsbeautifier', 'arch': 'python-jsbeautifier'},
    'kbxutil': {'debian': 'gnupg-utils'},
    'llvm-bcanalyzer': {'debian': 'llvm', 'arch': 'llvm'},
    'llvm-config': {'debian': 'llvm', 'arch': 'llvm'},
    'llvm-dis': {'debian': 'llvm', 'arch': 'llvm'},
    'ls': {'debian': 'coreutils', 'arch': 'coreutils'},
    'lsattr': {
        'debian': 'e2fsprogs',
        'arch': 'e2fsprogs',
        'FreeBSD': 'e2fsprogs',
    },
    'lz4': {'debian': 'lz4 | liblz4-tool', 'FreeBSD': 'lz4'},
    'msgunfmt': {
        'debian': 'gettext',
        'arch': 'gettext',
        'FreeBSD': 'gettext-tools',
    },
    'convert': {'debian': 'imagemagick', 'arch': 'imagemagick'},
    'nm': {'debian': 'binutils-multiarch', 'arch': 'binutils'},
    'objcopy': {'debian': 'binutils-multiarch', 'arch': 'binutils'},
    'objdump': {'debian': 'binutils-multiarch', 'arch': 'binutils'},
    'ocamlobjinfo': {'debian': 'ocaml-nox'},
    'odt2txt': {'debian': 'odt2txt', 'arch': 'odt2txt'},
    'oggDump': {'debian': 'oggvideotools'},
    'pgpdump': {'debian': 'pgpdump', 'arch': 'pgpdump'},
    'pdftotext': {
        'debian': 'poppler-utils',
        'arch': 'poppler',
        'FreeBSD': 'poppler-utils',
    },
    'pedump': {'debian': 'mono-utils', 'arch': 'mono', 'FreeBSD': 'mono'},
    'ppudump': {'debian': 'fp-utils', 'arch': 'fpc', 'FreeBSD': 'fpc'},
    'ps2ascii': {
        'debian': 'ghostscript',
        'arch': 'ghostscript',
        'FreeBSD': 'ghostscript9-base',
    },
    'readelf': {'debian': 'binutils-multiarch', 'arch': 'binutils'},
    'rpm2cpio': {
        'debian': 'rpm2cpio',
        'arch': 'rpmextract',
        'FreeBSD': 'rpm2cpio',
    },
    'Rscript': {'debian': 'r-base-core', 'arch': 'r'},
    'showttf': {'debian': 'fontforge-extras'},
    'sng': {'debian': 'sng'},
    'ssconvert': {'debian': 'gnumeric', 'arch': 'gnumeric'},
    'ssh-keygen': {'debian': 'openssh-client', 'arch': 'openssh'},
    'stat': {'debian': 'coreutils', 'arch': 'coreutils'},
    'sqlite3': {'debian': 'sqlite3', 'arch': 'sqlite', 'FreeBSD': 'sqlite3'},
    'wasm2wat': {'arch': 'wabt'},
    'tar': {'debian': 'tar', 'arch': 'tar'},
    'tcpdump': {'debian': 'tcpdump', 'arch': 'tcpdump'},
    'unsquashfs': {
        'debian': 'squashfs-tools',
        'arch': 'squashfs-tools',
        'FreeBSD': 'squashfs-tools',
    },
    'xxd': {
        'debian': 'xxd | vim-common',
        'arch': 'vim',
        'FreeBSD': 'vim | vim-lite',
    },
    'xz': {'debian': 'xz-utils', 'arch': 'xz'},
    'zipinfo': {'debian': 'unzip', 'arch': 'unzip', 'FreeBSD': 'unzip'},
    'zipnote': {'debian': 'zip'},
    'procyon': {'debian': 'procyon-decompiler'},
    'dumpxsb': {'debian': 'xmlbeans'},
}

# May be populated at runtime by remapped names like
# readelf -> arm-none-eabi-readelf, etc
# diff -> gdiff, etc
REMAPPED_TOOL_NAMES = {}

# GNU programs whose names differ on some non-GNU systems such as FreeBSD etc
# AND where the CLI or output of the programs differ from the non-GNU system
# versions. In these cases, add them here and make sure you wrap uses of them
# in get_tool_name() to pick up the alternate names.
#
# If we only use POSIX CLI options and the output is identical to the system
# version (so that our tests don't break) then it's unnecessary to add it here.
GNU_TOOL_NAMES = {'diff', 'readelf', 'objcopy', 'objdump'}
