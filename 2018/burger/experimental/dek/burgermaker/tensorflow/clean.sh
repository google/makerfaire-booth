ARCH=mobilenet_1.0_128
OUTDIR=/tmp/retrain_arch_$ARCH
rm -rf $OUTDIR/output_* /tmp/checkpoint  /tmp/_retrain_checkpoint.* $OUTDIR/saved_models
