#!/bin/bash

set -e


svgsort a.svg a-res.svg --no-split --no-reverse --a4
echo ""
svgsort b.svg b-res.svg --no-split --no-reverse --a4
echo ""
svgsort c.svg c-res.svg --no-split --no-reverse --a4

svgsort a.svg a-res-dim.svg --dim=300x100
echo ""
svgsort b.svg b-res-dim.svg --dim=432x33
echo ""
svgsort c.svg c-res-dim.svg --dim=44x100


echo ""

svgsort paper4-l.svg paper4-l-res.svg --a4
echo ""
svgsort paper4-p.svg paper4-p-res.svg --a4

echo ""

svgsort linearx.svg linearx-sorted.svg --no-split --no-reverse --a4 --pad 0.1
echo ""
svgsort linearx.svg linearx-sorted-reverse.svg --a4
echo ""
svgsort linearx.svg linearx-sorted-repeat.svg --repeat --a4
echo ""

