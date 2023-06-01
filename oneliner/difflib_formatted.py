_ = (
    Match := __import__("collections").namedtuple("Match", "a b size"),
    _calculate_ratio := lambda matches, length: 2.0 * matches / length
    if length
    else 1.0,
    SequenceMatcher := type(
        "SequenceMatcher",
        (object,),
        {
            "__init__": lambda self, isjunk=None, a="", b="", autojunk=True: (
                setattr(self, "isjunk", isjunk),
                setattr(self, "a", None),
                setattr(self, "b", None),
                setattr(self, "autojunk", autojunk),
                self.set_seqs(a, b),
                None,
            )[-1],
            "set_seqs": lambda self, a, b: (self.set_seq1(a), self.set_seq2(b)),
            "set_seq1": lambda self, a: (
                [
                    lambda: None,
                    lambda: (
                        setattr(self, "a", a),
                        setattr(self, "matching_blocks", None),
                        setattr(self, "opcodes", None),
                    ),
                ][a is not self.a]()
            ),
            "set_seq2": lambda self, b: (
                [
                    lambda: None,
                    lambda: (
                        setattr(self, "b", b),
                        setattr(self, "matching_blocks", None),
                        setattr(self, "opcodes", None),
                        setattr(self, "fullchain", None),
                        self._chain_b(),
                    ),
                ][b is not self.b]()
            ),
            "_chain_b": lambda self: (
                b := self.b,
                setattr(self, "b2j", {}),
                b2j := self.b2j,
                [
                    (indices := b2j.setdefault(elt, []), indices.append(i))
                    for i, elt in enumerate(b)
                ],
                setattr(self, "bjunk", set()),
                junk := self.bjunk,
                isjunk := self.isjunk,
                [
                    lambda: None,
                    lambda: (
                        [
                            ([lambda: None, lambda: (junk.add(elt))][isjunk(elt)]())
                            for elt in b2j.keys()
                        ],
                        [(b2j.pop(elt)) for elt in junk],
                    ),
                ][bool(isjunk)](),
                setattr(self, "bpopular", set()),
                popular := self.bpopular,
                n := len(b),
                [
                    lambda: None,
                    lambda: (
                        ntest := n // 100 + 1,
                        [
                            (
                                [lambda: None, lambda: (popular.add(elt))][
                                    len(idxs) > ntest
                                ]()
                            )
                            for elt, idxs in b2j.items()
                        ],
                        [(b2j.pop(elt)) for elt in popular],
                    ),
                ][self.autojunk and n >= 200](),
            ),
            "find_longest_match": lambda self, alo=0, ahi=None, blo=0, bhi=None: (
                a := self.a,
                b := self.b,
                b2j := self.b2j,
                isbjunk := self.bjunk.__contains__,
                ahi := ahi if ahi is not None else len(a),
                bhi := bhi if bhi is not None else len(b),
                state := {"besti": alo, "bestj": blo, "bestsize": 0, "j2len": {}},
                nothing := [],
                [
                    (
                        j2lenget := state["j2len"].get,
                        newj2len := {},
                        breaking_state := {"h": False},
                        [
                            (
                                [
                                    lambda: (
                                        [
                                            lambda: None,
                                            lambda: (
                                                breaking_state.__setitem__("h", True)
                                            ),
                                        ][j >= bhi](),
                                        newj2len.__setitem__(j, j2lenget(j - 1, 0) + 1),
                                        k := newj2len[j],
                                        [
                                            lambda: None,
                                            lambda: (
                                                state.__setitem__("besti", i - k + 1),
                                                state.__setitem__("bestj", j - k + 1),
                                                state.__setitem__("bestsize", k),
                                            ),
                                        ][k > state["bestsize"]](),
                                    ),
                                    lambda: None,
                                ][breaking_state["h"] or j < blo]()
                            )
                            for j in b2j.get(a[i], nothing)
                        ],
                        state.__setitem__("j2len", newj2len),
                    )
                    for i in range(alo, ahi)
                ],
                breaking_state := {"h": False},
                [
                    (
                        [
                            lambda: (breaking_state.__setitem__("h", True),),
                            lambda: (
                                state.__setitem__("besti", state["besti"] - 1),
                                state.__setitem__("bestj", state["bestj"] - 1),
                                state.__setitem__("bestsize", state["bestsize"] + 1),
                            ),
                        ][
                            state["besti"] > alo
                            and state["bestj"] > blo
                            and isbjunk(b[state["bestj"] - 1])
                            and a[state["besti"] - 1] == b[state["bestj"] - 1]
                        ]()
                    )
                    for _ in __import__("itertools").takewhile(
                        lambda _: not breaking_state["h"],
                        __import__("itertools").cycle([False]),
                    )
                ],
                breaking_state.__setitem__("h", False),
                [
                    (
                        [
                            lambda: (breaking_state.__setitem__("h", True)),
                            lambda: (
                                state.__setitem__("bestsize", state["bestsize"] + 1),
                            ),
                        ][
                            state["besti"] + state["bestsize"] < ahi
                            and state["bestj"] + state["bestsize"] < bhi
                            and isbjunk(b[state["bestj"] + state["bestsize"]])
                            and a[state["besti"] + state["bestsize"]]
                            == b[state["bestj"] + state["bestsize"]]
                        ]()
                    )
                    for _ in __import__("itertools").takewhile(
                        lambda _: not breaking_state["h"],
                        __import__("itertools").cycle([False]),
                    )
                ],
                Match(state["besti"], state["bestj"], state["bestsize"]),
            )[-1],
            "get_matching_blocks": lambda self: (
                [
                    lambda: (self.matching_blocks),
                    lambda: (
                        la := len(self.a),
                        lb := len(self.b),
                        queue := [(0, la, 0, lb)],
                        matching_blocks := [],
                        breaking_state := {"h": False},
                        [
                            (
                                [
                                    lambda: (breaking_state.__setitem__("h", True),),
                                    lambda: (
                                        match_entry := queue.pop(),
                                        alo := match_entry[0],
                                        ahi := match_entry[1],
                                        blo := match_entry[2],
                                        bhi := match_entry[3],
                                        match_info := self.find_longest_match(
                                            alo, ahi, blo, bhi
                                        ),
                                        i := match_info[0],
                                        j := match_info[1],
                                        k := match_info[1],
                                        x := match_info,
                                        [
                                            lambda: None,
                                            lambda: (
                                                matching_blocks.append(x),
                                                [
                                                    lambda: None,
                                                    lambda: (
                                                        queue.append((alo, i, blo, j))
                                                    ),
                                                ][alo < i and blo < j](),
                                                [
                                                    lambda: None,
                                                    lambda: (
                                                        queue.append(
                                                            (i + k, ahi, j + k, bhi)
                                                        )
                                                    ),
                                                ][i + k < ahi and j + k < bhi](),
                                            ),
                                        ][bool(k)](),
                                    ),
                                ][bool(queue)]()
                            )
                            for _ in __import__("itertools").takewhile(
                                lambda _: not breaking_state["h"],
                                __import__("itertools").cycle([False]),
                            )
                        ],
                        matching_blocks.sort(),
                        state := {"i1": 0, "j1": 0, "k1": 0},
                        non_adjacent := [],
                        [
                            (
                                [
                                    lambda: (
                                        [
                                            lambda: (
                                                state.__setattr__(
                                                    "k1", state["k1"] + k2
                                                ),
                                            ),
                                            lambda: (
                                                non_adjacent.append(
                                                    (
                                                        state["i1"],
                                                        state["j1"],
                                                        state["k1"],
                                                    )
                                                )
                                            ),
                                        ][bool(state["k1"])](),
                                        state.__setitem__("i1", i2),
                                        state.__setitem__("j1", j2),
                                        state.__setitem__("k1", k2),
                                    ),
                                    lambda: (state.__setitem__("k1", state["k1"] + k2)),
                                ][
                                    state["i1"] + state["k1"] == i2
                                    and state["j1"] + state["k1"] == j2
                                ]()
                            )
                            for i2, j2, k2 in matching_blocks
                        ],
                        [
                            lambda: False,
                            lambda: (
                                non_adjacent.append(
                                    (state["i1"], state["j1"], state["k1"])
                                ),
                            ),
                        ][bool(state["k1"])](),
                        non_adjacent.append((la, lb, 0)),
                        setattr(
                            self,
                            "matching_blocks",
                            list(map(Match._make, non_adjacent)),
                        ),
                        self.matching_blocks,
                    )[-1],
                ][self.matching_blocks is None](),
            )[-1],
        },
    ),
)
