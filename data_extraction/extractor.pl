#!/usr/bin/perl

use strict;
use warnings;
use feature "switch";

my $line;
my $telnum;

# buffer the last 100 lines
my @buf;

sub push_buf {
    push @buf, $_[0];
    if (scalar(@buf) == 100) { shift @buf; }
}

# convert month word to number
sub FebTo2 {
    given ($_[0]) {
	when ( /January/ ) {
	    return 1;
	}
	when ( /Feburary/ ) {
	    return 2;
	}
	when ( /March/ ) {
	    return 3;
	}
	when ( /April/ ) {
	    return 4;
	}
	when ( /May/ ) {
	    return 5;
	}
	when ( /June/ ) {
	    return 6;
	}
	when ( /July/ ) {
	    return 7;
	}
	when ( /August/ ) {
	    return 8;
	}
	when ( /September/ ) {
	    return 9;
	}
	when ( /October/ ) {
	    return 10;
	}
	when ( /November/ ) {
	    return 11;
	}
	when ( /December/ ) {
	    return 12;
	}
    }
}


# format date
sub format_date {
    my $pattern1 = "(January|Feburary|March|April|May|June|July|August|September|October|November|December)\\s+(\\d{4})";
    my $pattern2 = "(January|Feburary|March|April|May|June|July|August|September|October|November|December)\\s+(\\d+),\\s+(\\d{4})";
    my $month;
    given ($_[0]) {
	when ( /$pattern1/ ) {
	    $month = FebTo2($1);
	    if ($month == 2) {
		return $2 . "-" . $month . "-" . "28";
	    } else {
		return $2 . "-" . $month . "-" . "30";
	    }
	}
	when ( /$pattern2/ ) {
	    $month = FebTo2($1);
	    return $3 . "-" . $month . "-" . $2;
	}
    }
}

sub filter {
    my $temp = $_[0];
    $temp =~ s/Price to Compare//;
    $temp =~ s/\s+Yes: \$150 \(unless//;
    $temp =~ s/\s+PECO//;
    $temp =~ s/\s+Duquesne Price to//;
    $temp =~ s/\s+Duquesne//;
    return $temp;
}


# skip the first 3 telphone nums
my $n = 0;
while ( $line = <STDIN> ) {
    chomp $line;
    push_buf $line;
    if ($line =~ m/^(1\-\d{3}\-\d{3}\-\d{4})/) {
	if ($n++ > 2) {
	    last;
	}
    }
}

while ( $line ) {
    if ( $line =~ m/^(1\-\d{3}\-\d{3}\-\d{4})/ ) {
	$telnum = $1;
	my $output;
	if ( $buf[-2] =~ m/^\s+/ ) {
	    $output = $telnum . ":" . $buf[-3] . $buf[-2];
	    $output = filter($output);
#	    print "\n", $output, "\n";
	} else {
	    $output = $telnum . ":" . $buf[-2];
	    $output = filter($output);
#	    print "\n",  $output, "\n";
	}
	while ( $line = <STDIN> ) {
	    chomp $line;
	    push_buf $line;
	    given ($line) {
	      when ( /^1\-\d{3}\-\d{3}\-\d{4}/ ) {
		  last;
	      }
	      when ( /^Fixed price: (\d+) month term\*?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+Yes: \$(\d+)/ ) {
#		      print "Fixed price: $1 month(s) $2 cents with fee \$$3\n";
		      print $output, ":0:$1:::$2:$3\n";
	      }
	      when ( /^Fixed price: (\d+) month term\*?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}/ ) {
#		  print "Fixed price: $1 month(s) $2 cents\n";
		  print $output, ":0:$1:::$2:\n";
	      }
	      when ( /^Fixed price: (\d+) year term\*?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+Yes: \$(\d+)/ ) {
#		  print "Fixed price: $1 year(s) $2 cents with fee \$$3\n";
		  print $output, ":1::$1::$2:$3\n";
	      }
	      when ( /^Fixed price: (\d+) year term\*?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}/ ) {
#		  print "Fixed price: $1 year(s) $2 cents\n";
		  print $output, ":1::$1::$2:\n";
	      }
	      when ( /^Fixed price through (the)?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+Yes: \$(\d+)/ ) {
		  $line = <STDIN>;
		  chomp $line;
		  my $date = format_date($line);
#		  print "Fixed price through $line: $2 cents with fee \$$3\n";
		  print $output, ":2:::$date:$2:$3\n";
	      }
	      when ( /^Fixed price through (the)?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}/ ) {
		  $line = <STDIN>;
		  chomp $line;
#		  print "Fixed price through $line: $2 cents\n";
		  my $date = format_date($line);
		  print $output, ":2:::$date:$2:\n";
	      }
	      when ( /^Monthly variable price\*?\s+(\d+\.\d{2}) ¢\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}\s+\$\d+\.\d{2}/ ) {
#		  print "Monthly variable price: $1 cents\n";
		  print $output, ":3::::$1:\n"
	      }
	      when ( /^\*/ ) {
		  print "#$line\n";
	      }
	      when ( /(\d+)\% renewable/ ) {
		  print "#$1% renewable\n";
	      }
	    }
	}
    }
}

