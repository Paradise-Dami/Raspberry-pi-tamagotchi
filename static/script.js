async function boire() {
    try {
    await fetch('/boire', {method: 'POST'});
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function nourrir() {
    try {
    await fetch('/nourrir', {method: 'POST'});
    } catch (error) {
        console.error('Error fetching data:', error);
}
}


async function fetchData() {
    try {
        const response = await fetch('/get_db');
        const data = await response.json();
        console.log(data);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

