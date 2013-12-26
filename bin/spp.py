#!/usr/bin/env python

# Copyright (c) 2011, Incubaid BVBA
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Incubaid BVBA nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INCUBAID BVBA "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INCUBAID BVBA OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
import os.path
import optparse

import docutils
import docutils.core

# For side-effects
import sphinx
import sphinx.directives

LINE_OFFSET = 2

class CodeNodeVisitor(docutils.nodes.SparseNodeVisitor):
    def __init__(self, language, document):
        docutils.nodes.SparseNodeVisitor.__init__(self, document)

        self.language = language
        self.code_nodes = []

    def visit_literal_block(self, node):
        if self.language is not None:
            if node.attributes.get('language', None) != self.language:
                return

        self.code_nodes.append(node)


def extract_code(language, document):
    visitor = CodeNodeVisitor(language, document)
    document.walk(visitor)

    if not visitor.code_nodes:
        raise ValueError('No code nodes')

    for node in visitor.code_nodes:
        if len(node.children) != 1:
            raise ValueError('Multi-child node')

        yield node.line, node.rawsource


def main(language, source, source_path, output):
    _, pub = docutils.core.publish_programmatically(
        source_class=docutils.io.FileInput, source=source,
        source_path=source_path,
        destination_class=docutils.io.NullOutput, destination=None,
        destination_path=output,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=None, writer_name='null',
        settings=None, settings_spec=None, settings_overrides=None,
        config_section=None, enable_exit_status=True)

    for line, part in extract_code(language, pub.writer.document):
        output.write('{-# LINE %d "%s" #-}\n' % ((line + LINE_OFFSET),
            source_path))
        output.write(part)
        output.write('\n\n')


if __name__ == '__main__':
    parser = optparse.OptionParser()
    try:
        parser.remove_option('-h')
    except ValueError:
        pass

    parser.add_option('-h', dest='source')

    options, args = parser.parse_args()

    if len(args) == 0:
        source = sys.stdin
        source_path = '<stdin>'
        output_fd = sys.stdout
    elif len(args) != 2:
        parser.error('invalid number of arguments')
    else:
        source = open(args[0], 'rU') # closed by docutils!
        source_path = options.source
        output_ = args[1]

        assert not os.path.isfile(output_)

        output_fd = os.open(output_, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        output_fd = os.fdopen(output_fd, 'w')

    try:
        main(None, source, source_path, output_fd)
    finally:
        output_fd.close()