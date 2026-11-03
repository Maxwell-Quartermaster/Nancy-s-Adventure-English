# Thumbnail test, shirts v1 (t753u)

Every shirt mock-up was rendered at 150 px and 300 px wide (1x pixels, no retina) in
`thumbs-front-v1.png` and `thumbs-back-v1.png`. I looked at both images.

## Backs (1C/1D soft, 1F/1G tough, plus 1C on charcoal)
- **300 px: PASS.** Every bot reads right away by color and silhouette (orange pumpkin, green wedge, violet star with hat, blue cloud, brown square). All five names are legible.
- **150 px: PASS for the bot, but the names are only marginal.** The bot and the square border read from across a room. The name is about 6 px tall and only reads if you look closely.
  - Fix applied: the print is 12 in square, the max for a standard back, and the bot fills it. All five names share one size (12.5 units, about 1.4 in), the largest that fits "Quartermaster".
  - Not fixed: a bigger name would break the one-size-for-all-five rule or push the print past 12 in. The name is meant to be secondary.
- The tough versions (F/G) read slightly better at 150 px. The purple keyline and ink outline separate the bot from the black shirt.
- Black vs charcoal: black makes the purple and neon pop more. Charcoal looks softer and slightly washed out.

## Fronts (F1-F3 shared figure, nA/nB/nE per bot, F1 on charcoal)
- **True-scale fronts at 150 and 300 px: FAIL as a thumbnail, by design.** The chest mark is 1.75 in, polo-badge size (t747u "really subtle"), so in a thumbnail it is a colored dot on the chest. Making the mark bigger would break Maxwell's brief.
- **Fix applied:** added listing-style versions ("F1 + zoom", "nB + zoom", "nE + zoom") in the same thumbnail sheet. They show the shirt with a zoom bubble of the badge. The print itself is unchanged; the bubble is listing art only. At 150 px the bubble version clearly shows the ninja or the bot. **PASS.**
- The 001 under the mark is a quiet signature. It is legible in the close-ups and zoom bubbles but intentionally invisible at thumbnail size.

## Recommendation
Use a zoom-bubble image as the first listing photo for any front-led listing. Back-led listings can lead with the 300 px-class back image as is.
