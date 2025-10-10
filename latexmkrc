# Read key=value pairs from config file
my $config_file = "config/project_name.conf";
open(my $fh, '<', $config_file) or die "Cannot open $config_file: $!";
my %config;
while (my $line = <$fh>) {
    chomp($line);
    next if $line =~ /^\s*#/;      # skip comments
    next unless $line =~ /=/;      # skip invalid lines
    my ($key, $value) = split(/\s*=\s*/, $line, 2);
    $config{$key} = $value;
}
close($fh) or die "Could not close $config_file: $!";

my $mainfile = $config{'PROJECT_NAME'} // die "PROJECT_NAME not defined in $config_file\n";
$mainfile .= '.tex' unless $mainfile =~ /\.tex$/;

# Debug message
print ">> Using main file: $mainfile\n";

@default_files = ($mainfile);
$root_filename = $mainfile;

$biber = 'python3 makebib.py && biber %O %S';
# Use LuaLaTeX instead of pdfLaTeX
$pdflatex = 'lualatex --synctex=1 %O %S';
$pdf_mode = 1;    # produce PDF
