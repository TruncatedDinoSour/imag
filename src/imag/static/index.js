"use strict";

function vote(mode, id) {
    fetch(`/vote/${mode}/${id}`, { method: "POST" })
        .then((r) => {
            if (!r.ok) {
                alert("Failed to vote (keep in mind you can only vote once a day)");

                throw new Error(
                    `Failed to record the vote: ${r.status}`,
                );
            }

            return r.text();
        })
        .then((t) => {
            window.location.hash = id;
            document.write(t);
            document.close();
        })
        .catch((e) => console.error(e));
}
