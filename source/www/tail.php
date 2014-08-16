<?php
function follow($file)
{
    $size = 0;
    while (true) {
        clearstatcache();
        $currentSize = filesize($file);
        if ($size == $currentSize) {
            usleep(100);
            continue;
        }

        $fh = fopen($file, "r");
        fseek($fh, $size);

        while ($d = fgets($fh)) {
            echo $d;
        }

        fclose($fh);
        $size = $currentSize;
    }
}
follow('/var/log/sensord.log');
?>
