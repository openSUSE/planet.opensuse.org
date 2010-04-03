#!/usr/bin/perl
# script to convert the config.ini from PlanetPlanet to
# the rawdog feed format
#
# Pascal Bleser <pascal.bleser@opensuse.org>
# This script is licensed under the GPL v2.
#

use strict;
use warnings;
use Getopt::Long;

my $lang = undef;
GetOptions(
    "lang=s" => \$lang,
) || die "ERROR: $!";

my @feeds = ();
my $cf = undef;
while (<>) {
    chomp;
    s/\#.+$//;
    s/^\s*//;
    s/\s*$//;
    next if /^$/;
    if (/^\[\s*(.+:\/\/.+)\s*\]$/) {
        push(@feeds, $cf) if $cf;
        # section starts
        $cf = { 'feed' => $1 };
    } elsif ($cf) {
        my ($k, $v) = /^(.+?)\s*=\s*(.+)$/;
        print "? $_\n" unless $k && $v;
        $cf->{$k} = $v if $k && $v;
    }
}
push(@feeds, $cf) if $cf;

foreach my $f (@feeds) {
    my $face = undef;
    if (exists $f->{face}) {
        $face = $f->{face};
        if ($face =~ m|http://planet\.opensu\.se/(.+)$|) {
            $face = "hackergotchi/$1";
        }
    }

    print "feed 15m ",$f->{feed},"\n";
    print "\tdefine_name ",$f->{name},"\n";
    print "\tdefine_face ",$face,"\n" if $face;
    print "\tdefine_irc  ",$f->{irc},"\n" if exists $f->{irc};
    print "\tdefine_lang ",$lang,"\n" if defined $lang;
    print "\n";
}
