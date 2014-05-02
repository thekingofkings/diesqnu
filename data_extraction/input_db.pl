#!/usr/bin/perl

use warnings; 
use DBI;

## mysql user database name
$db ="ist510quote";
## mysql database user name
$user = "ist510";
 
## mysql database password
$pass = "ist510";
 
## user hostname : This should be "localhost" but it can be diffrent too
$host="jessieli-ubuntu.ist.psu.edu";
 
## SQL insert
my $query; 

$dbh = DBI->connect("DBI:mysql:$db:$host", $user, $pass);

my $line;
my $id = 0;
while ($line = <STDIN>) {
    chomp $line;
    my ($telnum, $name, $type, $month, $year, $date, $price, $fee, $annotation) = split ":", $line;

    if (!$month) { $month = "NULL"; }
    if (!$year) { $year = "NULL"; }
    if (!$date) { $date = "NULL"; }
    else { $date = "\"" . $date . "\""; }
    if (!$fee) { $fee = "NULL"; }
    if (!$annotation) { $annotation = "NULL"; }
    else { $annotation = "\"" . $annotation . "\""; }

    $query = "insert elecguide VALUES ($id, \"$name\", \"$telnum\", $type, $month, $year, $date, $price, $fee, $annotation)";
    print $query, "\n";
    $sqlQuery  = $dbh->prepare($query)
	or die "Can't prepare $query: $dbh->errstr\n";
 
    $rv = $sqlQuery->execute
	or die "can't execute the query: $sqlQuery->errstr";
    $id++;
}

$rc = $sqlQuery->finish;
exit(0);

