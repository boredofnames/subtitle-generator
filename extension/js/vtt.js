const fetchVtt = async (url) => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const response = await fetch("http://127.0.0.1:5000/vtt", {
        method: "POST",
        body: JSON.stringify({ url }),
        headers,
    });

    const data = await response.json()
    console.log(data)
    return data.vtt
}

export { fetchVtt }