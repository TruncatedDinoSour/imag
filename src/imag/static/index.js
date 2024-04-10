"use strict";

function vote(mode, id) {
    fetch(`/vote/${mode}/${id}`, { method: "POST" })
        .then((r) => {
            if (!r.ok) {
                alert(
                    "Failed to vote (keep in mind you can only vote once a day)",
                );

                throw new Error(`Failed to record the vote: ${r.status}`);
            }

            fetch(`/api/image/${id}`)
                .then((r) => {
                    if (!r.ok) {
                        alert("Failed to get current vote score");

                        throw new Error(
                            `Failed to fetch the vote score: ${r.status}`,
                        );
                    }

                    return r.json();
                })
                .then((j) => {
                    document.getElementById(`score-${id}`).innerText = j.score;
                })
                .catch((e) => console.error(e));
        })
        .catch((e) => console.error(e));
}
