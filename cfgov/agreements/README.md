# Credit Card Agreement Database

This django application powers CFPB's database of credit card agreements.

## Loading Agreements

This process depends on a number of conventions.

1. A directory of the latest quarter agreements provided
2. There is a PDF version of each agreement
3. The "metadata" available that describes the agreements, is based of the directory structure (see example below)
4. These files are uploaded to S3
5. The URL's are structured so that PDF's are in {root url}/pdf/{file_name}.pdf

## Example Directory Structure

```
American Express
    |->
        AmericanExpressGoldCard.pdf
        AmericanExpressGreenCard.pdf
        Ameriprise_Gold.pdf
Bank Of America
    |->
        American Express Preferred.pdf
        Visa Signature-World MasterCard.pdf
        Visa-MasterCard Classic Gold-Platinum.pdf
```

The actual loading process is then pretty simple:

`./manage.py import\_agreements --path /path/to/agreements`

This will wipe out the existing agreement database, and load the new metadata.
