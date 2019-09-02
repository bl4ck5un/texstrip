#!/usr/bin/env python


import argparse
import io
import ply.lex
import logging

# Usage
# python stripcomments.py input.tex > output.tex
# python stripcomments.py input.tex -e encoding > output.tex

def strip_comments(source):
    tokens = (
        'PERCENT', 'BEGINCOMMENT', 'ENDCOMMENT', 'BACKSLASH',
        'CHAR', 'BEGINVERBATIM', 'ENDVERBATIM', 'NEWLINE', 'ESCPCT',
    )
    states = (
        ('linecomment', 'exclusive'),
        ('commentenv', 'exclusive'),
        ('verbatim', 'exclusive')
    )

    # Deal with escaped backslashes, so we don't think they're escaping %.
    def t_BACKSLASH(t):
        r"\\\\"
        logging.debug('handling backslash at {}'.format(t.lexer.lineno))
        return t

    # One-line comments
    def t_PERCENT(t):
        r"\%"
        t.lexer.begin("linecomment")

    # Escaped percent signs
    def t_ESCPCT(t):
        r"\\\%"
        return t

    # Comment environment, as defined by verbatim package
    def t_BEGINCOMMENT(t):
        r"\\begin\s*{\s*comment\s*}"
        logging.debug('entering a comment environment at line {}'.format(t.lexer.lineno))
        t.lexer.begin("commentenv")

    # Verbatim environment (different treatment of comments within)
    def t_BEGINVERBATIM(t):
        r"\\begin\s*{\s*verbatim\s*}"
        t.lexer.begin("verbatim")
        return t

    # Any other character in initial state we leave alone
    def t_CHAR(t):
        r"."
        return t

    def t_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    # End comment environment
    def t_commentenv_ENDCOMMENT(t):
        r"\\end\s*{\s*comment\s*}"
        # Anything after \end{comment} on a line is ignored!
        t.lexer.begin('linecomment')

    # Ignore comments of comment environment
    def t_commentenv_CHAR(t):
        r"."
        pass

    def t_commentenv_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # End of verbatim environment
    def t_verbatim_ENDVERBATIM(t):
        r"\\end\s*{\s*verbatim\s*}"
        t.lexer.begin('INITIAL')
        return t

    # Leave contents of verbatim environment alone
    def t_verbatim_CHAR(t):
        r"."
        return t

    def t_verbatim_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    # End a % comment when we get to a new line
    def t_linecomment_ENDCOMMENT(t):
        r"\n"
        t.lexer.lineno += len(t.value)
        t.lexer.begin("INITIAL")
        # Newline at the end of a line comment is stripped.

    # Ignore anything after a % on a line
    def t_linecomment_CHAR(t):
        r"."
        pass

    lexer = ply.lex.lex()
    lexer.input(source)

    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break  # No more input
    #     print("({}, {}, {})".format(tok.type, repr(tok.value), tok.lineno, tok.lexpos))

    return u"".join([tok.value for tok in lexer])


def strip_comments_from_files(infile, outfile):
    with io.open(infile, encoding='utf-8') as f:
        source = f.read()

    with io.open(outfile, mode='w', encoding='utf-8') as f:
        f.write(strip_comments(source))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the file to strip comments from')
    parser.add_argument('--encoding', '-e', default='utf-8')
    parser.add_argument('--output', '-o', default='stripped.tex')

    args = parser.parse_args()

    with io.open(args.filename, encoding=args.encoding) as f:
        source = f.read()

    with io.open(args.output, mode='w', encoding=args.encoding) as f:
        f.write(strip_comments(source))


if __name__ == '__main__':
    main()
