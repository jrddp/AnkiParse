# AnkiParse

AnkiParse is a versatile script for creating [Anki](https://apps.ankiweb.net/) flashcards from plain text using a simple syntax. AnkiParse intends to create a bridge between note-taking and flashcard creation, allowing flashcards to be created easily while taking notes, and then later reformatted to be more visually appealing.

## Getting Started
- Install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin for Anki
- Clone this github repository
- Zip together all .py files and run using Python3
> If you have access to a POSIX compliant shell, you may use `build.sh` to creating an executable file

## Command Usage
`(python3) anki-parse -r [file]`
### -r flag
Adding -r to the command will enable in-file reformatting. By default, anki-parse will not make any changes to the original file.
With the -r flag, any syntax in the file will be replaced with more pleasing formatting using markdown.

Cards are only reformatted if they are successfully added to Anki.

### [file] argument

This is the text file that includes the relevant notes and cards.


## Syntax
AnkiParse works by adding the following commands into your syntax. All commands begin with a `!` at the start of a new line.

Cards are created and added by opening the cards using the `!q` command, and then eventually closing them with any added data once either `!f` or another `!q` is hit.

### Deck: !d
> Usage: `!d[c] {DECK}[::SUBDECK]` \
> OR `!dt {TAG1} {TAG2}...`

Sets the deck that any following cards will be added to

#### Create deck argument: c
Ensures that the specified deck is created if it does not already exist.

#### File-wide Tag Argument: t
Changes behavior to setting the default tags to be added onto every card defined in the file after the command.
If this is used again later in the file, the original tags will be overridden.
Tags are separated by whitespace.

These default tags can be nested depending on how many 't's are in the arguments.
For example, `!dt` is one level of tags and `!dtt` is another, which can be modified independently.

### Question: !q
> Usage: `!q[qtf] {BODY}`

Opens a new card with `{BODY}` as the front side text

If an existing card is opened, it will be finalized

`{BODY}` can be multiple lines, and will finalize upon the next given command.

#### Reverse Card Argument: q
Changes behavior to also add the reverse of the created card. Will not affect Cloze cards.

#### True or False Arguments: t or f
Will automatically build a card prefaced with "True or False:", and set the front of the card to "True" (for arg t) and "False" (for arg f)

### Answer: !a
> Usage: `!a {BODY}`

Adds `{BODY}` as the back side text of the opened card

### Replace: !r
> Usage: `!r[s] {REP1}///{REP2}...`

Replaces any "___" (3 underscores) with `{REP}` as a Cloze deletion.

If there are multiple "___", multiple replacements can be seperated by "///". By default, one card will be created hiding all replacements.

Having any `!r` perform on an open card will change it to a Cloze card.

Performing multiple `!r` on the same card will result in different Cloze groupings for each command.

#### Sequential Argument: `s`
Changes behavior of multiple replacements to create individual cards for each replacement, rather than one card for all replacements

### Tag: !t
> Usage: `!t[t] {TAG1} {TAG2}...`

Add anki tags to your card (Space seperated)

### Finalize: !f
> Usage: `!f`

Finalizes the currently open card

### Repeat: `!!`
> Usage: `!![at]`

Will use the same values for the last `a` or `t` called for the current card.

## Autoformatting
### Markdown Bold/Italics
Markdown &ast;&ast;**bold**&ast;&ast; and &ast;*italics*&ast; will be converted to HTML formatting.

Formatting using underscores  (&#95;&#95;**bold**&#95;&#95; and &#95;*italics*&#95;) are not supported.

### Markdown Images
Any valid markdown-formatted image will automatically be uploaded to Anki and attached to the card.

### Markdown Code Blocks
Any markdown-formatted code blocks will automatically be formatted when creating the card, so long as the respective language is included.

### LaTeX
Since Anki has better support for MathJax than LaTeX, using `$MATH$` or `$$MATH$$` will automatically transform into their MathJax formats when a card is created.
