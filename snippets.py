# Get the prominent words from a context, starting from a synsetid in input '<pos>.<offset>'
def get_prominent_words(ssid):
    if ssid == None:
        return None
    parts = ssid.split('.')
    return list(ss_ctx(wn.synset_from_pos_and_offset(pos=parts[0], offset=int(parts[1])))[:5])

# Annotate every disambiguated frame with the prominent words from the items's synsetid
wholedata = []
for frame in annotated_frames:
    result = {'frame_name': "", 'frame_elements': {}, 'lexunits': {}}
    oldn = frame['frame_name']
    print(oldn[0])
    words = get_prominent_words(oldn[1])
    result['frame_name'] = (oldn[0], oldn[1], words)
    for fe in frame['frame_elements'].keys():
        oldval = frame['frame_elements'][fe]
        fewrds = get_prominent_words(frame['frame_elements'][fe])
        result['frame_elements'][fe] = (oldval, fewrds)

    for lu in frame['lexunits'].keys():
        oldval = frame['lexunits'][lu]
        luwrds = get_prominent_words(frame['lexunits'][lu])
        result['lexunits'][lu] = (oldval, luwrds)
    wholedata.append(result)

# Get definition and id from WordNet Search, makes it clear if there's only one result
def get_definition_and_id(text, pos, idx):
    sss = wn.synsets(text, pos=pos)
    ss = sss[idx]
    if len(sss) == 1:
        print(f"--> ('{text}', '{ss.pos()}.{ss.offset()}'), <--")
    else:
        print(ss.definition())
        print(f"('{text}', '{ss.pos()}.{ss.offset()}'),")

# Used to print frame element names and definitions
def print_fe_def(frame):
    for fe in frame.FE.keys():
        print(fe)
        print(frame.FE[fe].definition)
        print()

# Used to print frame lexical units and definitions
def print_lu_def(frame):
    for lu in frame.lexUnit.keys():
        print(lu)
        print(frame.lexUnit[lu].definition)
        print()

# Used to check if (and when, the results from the lcs function mismatch)
def lcs_bugged(c1, c2, lcsfun=lcs_adapted):
    # Not sure if I can trust lcs, check it with this just in case
    orig = lcsfun(c1, c2)
    nltkimp = c1.lowest_common_hypernyms(c2)
    bugged = (orig != None and nltkimp != []
              ) and orig[0] != nltkimp[0] and (nltkimp[0] not in orig)
    if bugged and debug:
        print()
        print(f"{pp.bold('concepts')}:", c1, c2)
        print(f"{pp.bold('original')}:", orig)
        print(f"{pp.bold('nltk')}:", nltkimp)
    return bugged
