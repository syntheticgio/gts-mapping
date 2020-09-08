import argparse
import csv


def main(gts_file, go_file, output_file, separator):
    # Read in Go FILE into memory - this is the easiest way to deal with it given constrained data.
    with open(go_file, "r") as go_file_handle:
        go_file_csv = csv.reader(go_file_handle, delimiter="\t")
        next(go_file_csv) # Skip the header
        # Lets record all of the go to map info as a dictionary of list entries
        go_data = {}
        for row in go_file_csv:
            if row[0] in go_data:
                # Already there, additional GO term to add
                go_data[row[0]].append(row[3])
            else:
                # Not already entered, lets create it!
                go_data[row[0]] = []
                go_data[row[0]].append(row[3])
    #
    # If you want, you can uncomment the below line to have a printout of all of the GO TERMs in dictionary form
    #print(go_data)

    # Open the output file in the greater scope to let python deal with the cleanup
    # We could edit this in place, but always good to have a backup in case something goes wrong
    with open(output_file, 'w') as output_file_handle:
        # Lets make it a CSV file by using the built in CSV WRITER functionality instead of doing this by hand
        output_file = csv.writer(output_file_handle, delimiter="\t")
        # Open the GTS file.  We will read line by line and append any of the GO TERMS found for
        # that Accession number as a new last column of the file.
        with open(gts_file, 'r') as gts_file_handle:
            gts_file_csv = csv.reader(gts_file_handle, delimiter="\t")
            # We will want to get the header to re-write back into the output file
            need_header = True
            for row in gts_file_csv:
                if need_header:
                    # Haven't printed the header yet, so lets do that
                    need_header = False
                    # Write out header to the output file.
                    row.append("GO_TERM")
                    output_file.writerow(row)
                    continue
                # Map to the UniprotKB Accession number
                if row[0] in go_data:
                    # The AC is found in the go data!
                    # Get terms in semi-colon separated form
                    go_terms = ";".join(go_data[row[0]])
                    # Add to row as new column
                    row.append(go_terms)
                    # Write out to file
                    output_file.writerow(row)
                else:
                    # No GO Term data, add empty column and move on.
                    row.append("")
                    output_file.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands for mapping script.')
    parser.add_argument('gts_file',
                        help='The GTS file')
    parser.add_argument('go_file',
                        help='The Go File')
    parser.add_argument('output_file',
                        help='Output File')
    parser.add_argument('--separator', '-s',
                        default=";",
                        help="The separator that should be used in the Go Term column between entries.")
    args = parser.parse_args()

    main(args.gts_file, args.go_file, args.output_file, args.separator)

