# use strict;
use LWP::Simple qw( $ua );
use Text::CSV;
use List::MoreUtils qw(uniq);
# use warnings;

# This works sufficiently, but still need to delete lines with "," in them in the output.

my $csv = Text::CSV->new({ sep_char => ',' });
my $ATP_structures = 'tabularResults.csv';
my @ATP_PDBs = ('');
my @uniprot_IDs = ('');
my @all_PDBS_from_uniprot_IDs = ('');

open(my $data, '<', $ATP_structures) or die "Could not open '$ATP_structures' $!\n";
while (my $line = <$data>) {
  chomp $line;

  if ($csv->parse($line)) {
 
      my @fields = $csv->fields();
      push @ATP_PDBs, $fields[0];
      push @uniprot_IDs, $fields[3];
 
  } else {
      warn "Line could not be parsed: $line\n";
  }
}

# foreach (@uniprot_IDs)
for $i (0..scalar @uniprot_IDs) 
# for $i (0..4)
{

my $XML_query = qq(
<?xml version="1.0" encoding="UTF-8"?>

<orgPdbQuery>
    <version>B0905</version>
    <queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
    <description>Simple query for a list of Uniprot Accession IDs: $uniprot_IDs[$i]</description>
    <accessionIdList>$uniprot_IDs[$i]</accessionIdList>
</orgPdbQuery>
);
    # print "\nquery:", $XML_query;

    my $request = HTTP::Request->new( POST => 'http://www.rcsb.org/pdb/rest/search/');
    $request->content_type( 'application/x-www-form-urlencoded' );
    $request->content( $XML_query );
    my $response = $ua->request( $request );

    # Print response content in either case
    # print " ", $uniprot_IDs[$i];
    # print " ", $response->content;
    if ($response->content =~ m/Problem/) 
    {
        # print "Skipping ", $uniprot_IDs[$i];
    }
    else 
    {
        # The data is returned with something (chain ID?) appended after a colon.
        # We need to remove that so we can compare with our list of ATP-containing PDBs.
        my $tmp = $response->content; 
        if (substr($tmp, 0, 4) !~ /null/)
        {
            my @words = split ' ', $tmp;
            foreach (@words)
            {
                print "\n";
                print $uniprot_IDs[$i];
                print " ";
                $_ =~ s/:(.*)//g;
                print $_;
            }
            # $all_PDBS_from_uniprot_IDs[$i] = substr($tmp, 0, 4)
        }
    }
}
# print uniq @all_PDBS_from_uniprot_IDs
# foreach (uniq @all_PDBS_from_uniprot_IDs)
# {
#     print $_;
#     print "\n";
# }

# foreach $e (uniq @ATP_PDBs, uniq @all_PDBS_from_uniprot_IDs) {
#     $union{$e}++ && $isect{$e}++
# }
# @union = keys %union;
# @isect = keys %isect;

# print @union

foreach (uniq @all_PDBS_from_uniprot_IDs) {
    print $_;
    print "\n";
}