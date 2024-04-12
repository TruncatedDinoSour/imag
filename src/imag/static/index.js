/**
 * @file
 * @license
 * This is free and unencumbered software released into the public domain.
 * For more information, please refer to <http://unlicense.org/>
 */

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

function main() {
    console.log(
        "Originally made with <3 by Ari Archer <ari@ari.lt> on 2024/03/10, licensed under the Unlicense: https://ari.lt/gh/imag",
    );

    for (let img of document.getElementsByTagName("img"))
        img.title = img.alt;
}

document.addEventListener("DOMContentLoaded", main);
