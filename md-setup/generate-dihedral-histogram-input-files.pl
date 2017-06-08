#!/usr/bin/perl

$rn=$ARGV[0];
$res=$ARGV[1];

$aa{'ALA'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'ALA'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'ALA'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'ALA'}[3]=sprintf(":%.0f\@HB1 :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);

$aa{'ARG'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'ARG'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'ARG'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'ARG'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'ARG'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'ARG'}[5]=sprintf(":%.0f\@NE :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);
$aa{'ARG'}[6]=sprintf(":%.0f\@CZ :%.0f\@NE :%.0f\@CD :%.0f\@CG",$rn,$rn,$rn,$rn);
$aa{'ARG'}[7]=sprintf(":%.0f\@NH1 :%.0f\@CZ :%.0f\@NE :%.0f\@CD",$rn,$rn,$rn,$rn);

$aa{'SER'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'SER'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'SER'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'SER'}[3]=sprintf(":%.0f\@OG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);

$aa{'ASN'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'ASN'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'ASN'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'ASN'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'ASN'}[4]=sprintf(":%.0f\@ND2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'ASN'}[5]=sprintf(":%.0f\@HD21 :%.0f\@ND2 :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);

$aa{'ASP'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'ASP'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'ASP'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'ASP'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'ASP'}[4]=sprintf(":%.0f\@OD2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'CYS'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'CYS'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'CYS'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'CYS'}[3]=sprintf(":%.0f\@SG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'CYS'}[4]=sprintf(":%.0f\@HG :%.0f\@SG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'CYX'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'CYX'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'CYX'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'CYX'}[3]=sprintf(":%.0f\@SG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'CYX'}[4]=sprintf(":%.0f\@HG :%.0f\@SG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'GLN'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'GLN'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'GLN'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'GLN'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'GLN'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'GLN'}[5]=sprintf(":%.0f\@NE2 :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);
$aa{'GLN'}[6]=sprintf(":%.0f\@HE21 :%.0f\@NE2 :%.0f\@CD :%.0f\@CG",$rn,$rn,$rn,$rn);

$aa{'GLU'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'GLU'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'GLU'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'GLU'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'GLU'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'GLU'}[5]=sprintf(":%.0f\@OE1 :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);

$aa{'GLY'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'GLY'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'GLY'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);

$aa{'HIP'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'HIP'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'HIP'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'HIP'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'HIP'}[4]=sprintf(":%.0f\@CD2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'HID'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'HID'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'HID'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'HID'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'HID'}[4]=sprintf(":%.0f\@CD2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'HIE'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'HIE'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'HIE'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'HIE'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'HIE'}[4]=sprintf(":%.0f\@CD2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'HIS'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'HIS'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'HIS'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'HIS'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'HIS'}[4]=sprintf(":%.0f\@CD2 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'ILE'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'ILE'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'ILE'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'ILE'}[3]=sprintf(":%.0f\@CG1 :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'ILE'}[4]=sprintf(":%.0f\@CD1 :%.0f\@CG1 :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'LEU'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'LEU'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'LEU'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'LEU'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'LEU'}[4]=sprintf(":%.0f\@CD1 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'LYS'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'LYS'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'LYS'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'LYS'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'LYS'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'LYS'}[5]=sprintf(":%.0f\@CE :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);
$aa{'LYS'}[6]=sprintf(":%.0f\@NZ :%.0f\@CE :%.0f\@CD :%.0f\@CG",$rn,$rn,$rn,$rn);
$aa{'LYS'}[7]=sprintf(":%.0f\@HZ1 :%.0f\@NZ :%.0f\@CE :%.0f\@CD",$rn,$rn,$rn,$rn);

$aa{'MET'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'MET'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'MET'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'MET'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'MET'}[4]=sprintf(":%.0f\@SD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'MET'}[5]=sprintf(":%.0f\@CE :%.0f\@SD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);

$aa{'PHE'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'PHE'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'PHE'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'PHE'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'PHE'}[4]=sprintf(":%.0f\@CD1 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'PRO'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'PRO'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'PRO'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'PRO'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'PRO'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'PRO'}[5]=sprintf(":%.0f\@N :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);

$aa{'HYP'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'HYP'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'HYP'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'HYP'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'HYP'}[4]=sprintf(":%.0f\@CD :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'HYP'}[5]=sprintf(":%.0f\@N :%.0f\@CD :%.0f\@CG :%.0f\@CB",$rn,$rn,$rn,$rn);

$aa{'THR'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'THR'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'THR'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'THR'}[3]=sprintf(":%.0f\@CG2 :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'THR'}[4]=sprintf(":%.0f\@HG1 :%.0f\@OG1 :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'TRP'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'TRP'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'TRP'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'TRP'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'TRP'}[4]=sprintf(":%.0f\@CD1 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);

$aa{'TYR'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'TYR'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'TYR'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'TYR'}[3]=sprintf(":%.0f\@CG :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);
$aa{'TYR'}[4]=sprintf(":%.0f\@CD1 :%.0f\@CG :%.0f\@CB :%.0f\@CA",$rn,$rn,$rn,$rn);
$aa{'TYR'}[5]=sprintf(":%.0f\@HH :%.0f\@OH :%.0f\@CZ :%.0f\@CE1",$rn,$rn,$rn,$rn);

$aa{'VAL'}[0]=sprintf(":%.0f\@C :%.0f\@N :%.0f\@CA :%.0f\@C",$rn-1,$rn,$rn,$rn);
$aa{'VAL'}[1]=sprintf(":%.0f\@N :%.0f\@CA :%.0f\@C :%.0f\@N",$rn,$rn,$rn,$rn+1);
$aa{'VAL'}[2]=sprintf(":%.0f\@CA :%.0f\@C :%.0f\@N :%.0f\@CA",$rn,$rn,$rn+1,$rn+1);
$aa{'VAL'}[3]=sprintf(":%.0f\@CG1 :%.0f\@CB :%.0f\@CA :%.0f\@N",$rn,$rn,$rn,$rn);

$j=0;
for $i (0..$#{$aa{$res}}){
  if ($j == 0) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out phi$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 1) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out psi$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 2) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out omega$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 3) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out chi1$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 4) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out chi2$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 5) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out chi3$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 6) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out chi4$res$rn.dat prec 11.9\n";
  }
  elsif ($j == 7) {
  print "dihedral $res$rn-$j $aa{$res}[$i]\nhist $res$rn-$j,-180,180,6,* norm out chi5$res$rn.dat prec 11.9\n";
  }
  $j++;
}

