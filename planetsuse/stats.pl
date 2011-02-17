#!/usr/bin/perl
# vim: set ts=4 sw=4 et:
use strict;
use warnings;
my $has_plot = 0;
eval {
    use Imager::Graph::Pie;
    $has_plot = 1;
};

my %names = ();
my %feeds = ();
my @blocks = ();
my $cur = undef;
while (<STDIN>) {
    chomp;
    s/#.*$//;
    s/^\s*//;
    s/\s*$//;
    next if /^$/;

    if (/^feed\s+\S+\s+(.+)$/) {
        my $url = lc($1);
        $feeds{$url} = 1;
        push(@blocks, $cur) if defined $cur;
        $cur = { url => $1 };
    } elsif (/^define_(\S+)\s+(.+)$/) {
        my $key = $1;
        my $value = $2;
        die "define_$key before a feed block at $." unless defined $cur;
        $cur->{$key} = $value;
        if ($key eq 'name') {
            $value =~ s/\s+//g;
            $names{lc($value)} = 1;
        }
    }
}
push(@blocks, $cur) if defined $cur;
close(STDIN);

my %bylang = ();
{
    foreach my $b (@blocks) {
        my $l;
        if (exists $b->{lang}) {
            $l = $b->{lang};
        } else {
            $l = 'en';
        }
        $bylang{$l} = 0 unless exists $bylang{$l};
        $bylang{$l} = $bylang{$l} + 1;
    }
}

print scalar(@blocks), " blocks", "\n";
print scalar(keys(%names)), " bloggers", "\n";
print scalar(keys(%feeds)), " feeds", "\n";
print "By language:", "\n", join("\n", map { $_."=".$bylang{$_} } sort { $bylang{$b} - $bylang{$a} } keys %bylang), "\n";

if ($has_plot) {
    my $data = [];
    my $labels = [];
    foreach my $lang (sort { $bylang{$b} - $bylang{$a} } keys %bylang) {
        push(@$data, $bylang{$lang});
        push(@$labels, $lang);
    }
    my $tfont = Imager::Font->new(file => '/usr/share/fonts/truetype/DejaVuSansCondensed-Bold.ttf');
    my $lfont = Imager::Font->new(file => '/usr/share/fonts/truetype/DejaVuSansCondensed.ttf');
    my $pie = Imager::Graph::Pie->new;
    my $img = $pie->draw(
        data => $data,
        labels => $labels,
        font => $lfont,
        width => 400,
        height => 300,
        style => 'primary',
        back => 'FFFFFF',
        legend => {
            font => $lfont,
            fill => 'EEEEEE',
        },
        title => {
            text => 'Planet openSUSE by language',
            size => 18,
            font => $tfont,
            color => '000000',
            halign => 'center',
            valign => 'top',
        },
        features => ['labelspc', 'nolegend', 'nodropshadow', 'nooutline'],
    ) or die $pie->error;
    $img->write(file => 'stats.png');
} else {
    print "\n", "Install Imager::Graph to generate fancy graphs", "\n";
}


