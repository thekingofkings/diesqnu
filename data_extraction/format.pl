#!/usr/bin/perl

use strict;
use warnings;
use feature "switch";

my $line = <STDIN>;
my $nextline;
my $annotation;

while ($line && $line =~ m/^1\-\d{3}\-\d{3}\-\d{4}/) {
    chomp $line;
    $line .= ":";
    $nextline = <STDIN>;
    if ($nextline && $nextline =~ m/^#/) {
	while ($nextline =~ m/^#/) {
	    chomp $nextline;
	    $nextline =~ s/^#/ /;
	    $annotation .= $nextline;
	    $nextline = <STDIN>;
	}
	$line .= $annotation;
	$annotation = "";
    }
    print $line, "\n";
    $line = $nextline;
}
