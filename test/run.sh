#!/bin/bash

set -e


svgsort a.svg a-res.svg --no-split --dim=A4
echo ""
svgsort b.svg b-res.svg --no-split --dim=A4
echo ""
svgsort c.svg c-res.svg --no-split --dim=A4
echo ""

svgsort a.svg a-res-dim.svg --dim=300x100
echo ""
svgsort b.svg b-res-dim.svg --dim=432x33
echo ""
svgsort c.svg c-res-dim.svg --dim=44x100
echo ""

echo ""
svgsort a.svg a-res-no-adjust.svg --no-adjust
echo ""
svgsort b.svg b-res-no-adjust.svg --no-adjust
echo ""
svgsort c.svg c-res-no-adjust.svg --no-adjust
echo ""

svgsort parallel.svg parallel-res.svg --pen-moves
echo ""

svgsort paper4-l.svg paper4-l-res.svg --dim=A4
echo ""
svgsort paper4-p.svg paper4-p-res.svg --dim=A3
echo ""

svgsort linearx.svg linearx-sorted.svg --no-split --dim=A4 --pad 0.1
echo ""
svgsort linearx.svg linearx-sorted-moves.svg --dim=A4 --pen-moves
echo ""
svgsort linearx.svg linearx-sorted-repeat.svg --repeat --dim=A4

