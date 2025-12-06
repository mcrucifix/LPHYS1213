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

$nomencl_run = 'makeindex -s nomencl.ist -o %D %S';
$makeindex = $nomencl_run; # Set the general makeindex variable to handle the custom files

@default_files = ($mainfile);
$root_filename = $mainfile;

$biber = '~/.venvs/auto/bin/python3 makebib.py && biber %O %S';
# Use LuaLaTeX instead of pdfLaTeX
$pdflatex = 'lualatex --synctex=1 %O %S';
$pdf_mode = 1;    # produce PDF

# Custom dependency to run the Python script to generate figures
### add_cus_dep('py', 'pdf', 0, 'py2pdf');
### add_cus_dep('xp', 'eepic', 0, 'xp2eepic');
### add_cus_dep('svg', 'pdf_tex', 0, 'svg2pdftex');
### 
### sub py2pdf{
###   system("cd Python && python3 `basename $_[0]`.py");
### }
### 
### sub xp2eepic{
###   system("cd Xp && epix `basename $_[0]`.xp");
### }
### 
### sub svg2pdftex{
###   system("inkscape --export-filename=$_[0].pdf --export-latex $_[0].svg");
### }
### 
### 
### 
### # Tell latexmk that the generated figures (PDFs) are targets of the 'py' extension
### $clean_ext = 'py pdf';
### 
### # Custom dependency to convert SVG files in Pdftex/ to PDF and PDF_TEX
### # The command uses modern Inkscape syntax and includes the full path to the source SVG.
