# PyPWikt - Python Wiktionary Parser

PyPWikt is a Python package for parsing wiktionary pages. It extract specyfic information about words. In especially can be used for generating dictionaries (from one language to another).

## Supported languages
* English
* Polish

## Example
The simple usage example of PyPWikt can be found in cli.py script.

To translate English word "code" to Polish using Polish wiktionary page:
```
$ ./cli.py -w code -l pl -o en
code
	NOUN:
		MN: (1.1) [[kod]]
		MN: (1.2) [[norma]]
	VERB:
		MN: (2.1) [[kodować]]
```

To get all meanings of word "code" frome English wikitionary page:
```
$ ./cli.py -w code -l en -o en
code
	NOUN:
		MN: A short symbol, often with little relation to the item it represents.
			{{ux|en|This flavour of soup has been assigned the '''code''' WRT-9.}}
		MN: By [[synecdoche]]: a [[codeword]], [[code point]], an encoded representation of a [[character]], [[symbol]], or other entity.
			{{ux|en|The [[ASCII]] '''code''' of "A" is 65.}}
		MN: A message represented by rules intended to conceal its meaning.
			{{ux|en|Object-oriented C++ '''code''' is easier to understand for a human than C '''code'''.}}
			{{ux|en|I wrote some '''code''' to reformat text documents.}}
	VERB:
		MN: {{context|computing|lang=en}} To write software programs.
			''I learned to '''code''' on an early home computer in the 1980s.''
		MN: To [[categorise]] by assigning identifiers from a [[schedule]], for example CPT coding for medical insurance purposes.
		MN: {{context|cryptography|lang=en}} To [[encode]].
			''We should '''code''' the messages we sent out on Usenet.''
```
