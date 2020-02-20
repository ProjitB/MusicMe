import random
import argparse
import sys

FILENAME = 'sample_doc.txt'

def load_info(filename):
    mapping_a_s = {}
    mapping_s_a = {}
    artistlist = []
    songlist = []
    artist = ''
    with open(filename) as f:
        for line in f:
            if line[:3] == '---':
                artist = line[4:]
                artist = artist[:-5]
                artistlist.append(artist)
            else:
                if line != '' and line !='\n':
                    line.strip()
                    if line[-1] == '\n':
                        line = line[:-1]
                    try:
                        mapping_s_a[line].append(artist)
                    except:
                        mapping_s_a[line] = [artist]
                    try:
                        mapping_a_s[artist].append(line)
                    except:
                        mapping_a_s[artist] = [line]

                    songlist.append(line)
    f.close()

    artistlist = list(set(artistlist))
    songlist = list(set(songlist))
    return songlist, artistlist, mapping_a_s, mapping_s_a

def select_random_song(artistlist, songlist, mapping_s_a):
    song_num = random.randint(0, len(songlist)-1)
    songname = songlist[song_num]
    potential = mapping_s_a[songname]
    for a in potential:
        if a not in artistlist:
            potential.remove(a)
    if len(potential) == 0:
        return "No Song Found"
    artistnum = random.randint(0, len(potential)-1)
    artistname = mapping_s_a[songname][artistnum]
    return "{}: {}".format(artistname, songname)


def parse_args():
    parser = argparse.ArgumentParser(prog='Music Recommendation', usage = argparse.SUPPRESS, formatter_class=argparse.RawTextHelpFormatter, description="Recommends music based on file at {}".format(FILENAME))
    parser.add_argument('-a', '--artist', dest='artist', metavar='\b', help="Filter by artist")
    parser.add_argument('--tags', nargs='+', dest='tags', metavar='\b', help="Filter by tag(s). && of tags supplied.")
    parser.add_argument('-t', '--tag', dest='tag', metavar='\b', help="Filter by tag.")
    parser.add_argument('--all', dest='all', action='store_true', help="Print Everything that matches")
    try:
        args = parser.parse_args()
    except SystemExit as err:
        if err.code == 2:
            parser.print_help()
        sys.exit(0)
    return args


def extract_tags(song):
    lst = song.split('[')
    tags = lst[1:]
    if len(tags) == 0:
        return []
    return [t.replace(']', '').lower().strip() for t in tags]

def compare_sets(superset, subset):
    for s in subset:
        if s not in superset:
            return False
    return True

def check_artist(a_set, artist):
    tempaset = [a.lower().strip().replace(' ', '') for a in a_set]
    # print(tempaset, "-", artist)
    for a in tempaset:
        if artist in a:
            return True
    return False

def find_artist_index(alist, artist_cleaned):
    tempaset = [a.lower().strip().replace(' ', '') for a in alist]
    idxlist = []
    for i, a in enumerate(tempaset):
        if artist_cleaned in a:
            idxlist.append(i)
    return idxlist 

def select_all(songlist, artistlist, maps_a):
    strf = ""
    for song in songlist:
        for artist in maps_a[song]:
            if artist in artistlist:
                strf += "{}: {}\n".format(artist, song)
        # print(maps_a[song])
    if strf[-1] == "\n":
        strf = strf[:-1]
    return strf

def func_invoker(args, sl, al, mapa_s, maps_a):
    if args.artist:
        alist = list(al)
        artist_cleaned = args.artist.lower().strip().replace(' ', '')
        idxlist = find_artist_index(alist, artist_cleaned)
        if len(idxlist) == 0:
            return "Artist not Found"
        al = [al[idx] for idx in idxlist]
        # print(al)
        sllist = []
        for a in al:
            sllist += mapa_s[a]
        sl = sllist
        # print(mapa_s)
        # print("Cleaned: {}".format(artist_cleaned))
        # sl = [song for song in sl if check_artist(maps_a[song], artist_cleaned)]
        # print(sl)

    if args.tags:
        tagsearch = [t.lower().strip() for t in args.tags]
        sl = [song for song in sl if compare_sets(extract_tags(song), tagsearch)]

    if args.tag:
        tagsearch = [args.tag.lower().strip()]
        sl = [song for song in sl if compare_sets(extract_tags(song), tagsearch)]

    if len(sl) == 0:
        return "No Songs Found"

    if args.all:
        return select_all(sl, al, maps_a)
    return select_random_song(al, sl, maps_a)


def main():
    sl, al, mapa_s, maps_a = load_info(FILENAME)
    args = parse_args()
    print(func_invoker(args, sl, al, mapa_s, maps_a))

if __name__ == '__main__':
    main()


