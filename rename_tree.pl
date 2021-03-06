#!/usr/bin/env perl

#script to rename from 2 column file that has old name tab new name
#the new name cannot contain any of these characters or will mess up newick format ( , : ; ) 
#script from Kenosis @ biostars https://www.biostars.org/p/76972/

use strict;
use warnings;

my $treeFile = pop;
my %taxonomy = map { /(\S+)\s+(.+)/; $1 => $2 } <>;

push @ARGV, $treeFile;

while ( my $line = <> ) {
    $line =~ s/\b$_\b/$taxonomy{$_}/g for keys %taxonomy;
    print $line;
}
