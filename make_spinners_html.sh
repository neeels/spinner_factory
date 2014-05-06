#!/bin/sh
{

cat <<END
<html><body bgcolor="#666666">
<!--
ls -1 *.gif | xclip -i
:'<,'>s#.*#<img src="&" border="0"><br><br><br><br>#g
-->

<center>
END
for f in *.gif; do
  echo '<a name="'"$f"'"><br></a><br><br><br>'
  echo '<br><br><br><br>'
  echo '<img src="'"$f"'" border="0">'
  echo '<br><br><span style="font-size:11px; color: white">'"$f"'</span>'
  echo '<br><br><br><br>'
  echo '<br><br><br><br>'
  echo '<br><br><br><br>'
done

cat <<END
</center>
</body></html>
END

} > spinners.html
