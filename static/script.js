async function boire() {
    await fetch('/boire', {method: 'POST'});
}

async function nourrir() {
    await fetch('/nourrir', {method: 'POST'});
}
