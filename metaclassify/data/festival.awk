! /^http/ {
  tags[$1] = 1
}
/^http/ {
  system("wget --no-check-certificate \"" $1 "\"")
  for (t in tags) {
	system("mkdir -p /data/festival-of-giants-2017/" t)
        system("cp $(basename \"" $1 "\") /data/festival-of-giants-2017/" t)
  }
  delete tags
  system("rm -f $(basename \"" $1 "\")")
}
