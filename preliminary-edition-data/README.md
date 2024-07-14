## Preliminary Edition Data

This directory contains edition files prepared in XML for each of the five editions
 in the Frankenstein Variorum for machine-assisted collation. The files are freely available, but
we would appreciate your citing the Frankenstein Variorum project as their source. Please note that
the files in this directory contain no collation data, because they repreesent a first stage of 
text preparation necessary for the collation process.  

The markup in these editions is prepared to be part of the collation process, in order to:
* include its 
information about structure (paragraph and chapter boundaries, for example) together
with the content, 
* include markup of deletions and insertions from the manuscript material from the Shelley-Godwin Archive as 
well as in the Thomas Copy. 
* include boundary indicators for 33 collation units. Each edition was divided into units roughly the size of a chapter. 
This was designed to facilitate collation of the novel in aligned ”chunks” to help prevent errors. Each edition shares
`<anchor>` elements that mark the beginning of each collation unit, labeled with `@xml:id` attribute values of "C01" to "C33"

The files for the 1818 and 1831 texts were derived from the codebase for the Pennsylvania Electronic Edition.
They were transformed using Perl regular expresssions from their original HTML to a simple structure of XML that enabled us to follow the structure of volumes,
chapters, paragraphs, and lines of poetry, all of which were important to trace in the collation process. This
code was corrected on consulting photo facsimiles of each print edition.

The Thomas Copy was prepared from the XML of the 1818 text, and Elisa Beshero-Bondar added encoded data about handwritten
insertions, deletions, and marginal annotations on consulting the text held at the Pierpont Morgan Library, and making editorial decisions
based on Nora Crook's and James Rieger’s editions that include the Thomas Copy. 

The 1823 text was prepared from OCR of a photo facsimile by librarians at Carnegie Mellon University, 
and corrected by consulting the text. It was encoded in XML consisent with the markup of 
the 1818, 1831, and Thomas copy texts.

The files for the Shelley-Godwin Archive were combined together from their page-by-page structure
and to reposition marginal insertions, which had been encoded at the end of each file. We 
resequenced these following the xml:ids and pointers in the documents in order to position these
insertions and notes at their points of insertion as interpreted by the editors of the Shelley-Godwin Archive.
This permitted us to collate them in semantic reading sequence. The Shelley-Godwin archive code 



