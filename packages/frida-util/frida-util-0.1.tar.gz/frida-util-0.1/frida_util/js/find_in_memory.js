function memory_scan_match (match) {
    
    if ( match.length == 0 ) {
        return;
    }

    var address = match['address'];
    var size = match['size'];

    var d = {
        'address': address,
        'size': size
    };

    total_matches.push(d);
}

function memory_scan_completed () {

    if ( total_matches.length > 0 ) {
        send(total_matches);
    } else {
        send(null);
    }

}

// Add downselect to include module here
var search_space = Process;
var total_matches = [];
var protection = null;

setTimeout(function () {
    search_space.enumerateRangesSync('rw').forEach(
        function (range) {
            protection = Process.getRangeByAddress(range.base).protection;

            // Protection can actually change between enumerating at the execution of scan. Try to catch that.
            if ( protection == "rw-" || protection == "rwx" ) {
                Memory.scanSync(range.base, range.size, "SCAN_PATTERN_HERE").forEach( memory_scan_match );
            };
        });

    memory_scan_completed();
});
