#!/bin/bash

set -e


svgsort a.svg a-res.svg --no-split --no-reverse
echo ""
svgsort b.svg b-res.svg --no-split --no-reverse
echo ""
svgsort c.svg c-res.svg --no-split --no-reverse

svgsort a.svg a-res-dim.svg --dim=300x100
echo ""
svgsort b.svg b-res-dim.svg --dim=432x33
echo ""
svgsort c.svg c-res-dim.svg --dim=44x100


echo ""

svgsort paper4-l.svg paper4-l-res.svg
echo ""
svgsort paper4-p.svg paper4-p-res.svg

echo ""

svgsort linearx.svg linearx-sorted.svg --no-split --no-reverse
echo ""
svgsort linearx.svg linearx-sorted-reverse.svg
echo ""
svgsort linearx.svg linearx-sorted-repeat.svg --repeat
echo ""

