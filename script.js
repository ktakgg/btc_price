async function calculateValue() {
    const cryptoSymbol = document.getElementById('crypto_symbol').value.toUpperCase();
    const amount = parseFloat(document.getElementById('amount').value);
    const currency = document.getElementById('currency').value.toUpperCase();
    const resultDiv = document.getElementById('result');

    resultDiv.innerHTML = 'Calculating...'; // Clear previous results

    if (!cryptoSymbol || isNaN(amount) || amount <= 0) {
        resultDiv.innerHTML = '<p class="error">Please enter a valid cryptocurrency symbol and amount.</p>';
        return;
    }

    try {
        // Make a request to the backend
        const response = await fetch('/get_crypto_value', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                crypto_symbol: cryptoSymbol,
                amount: amount,
                currency: currency,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <p><strong>Symbol:</strong> ${data.symbol}</p>
                <p><strong>Price per unit (${data.currency}):</strong> ${data.price_per_unit.toFixed(2)}</p>
                <p><strong>Amount Owned:</strong> ${data.amount_owned}</p>
                <p><strong>Total Value (${data.currency}):</strong> ${data.total_value.toFixed(2)}</p>
            `;
        }
    } catch (error) {
        console.error('Error fetching crypto value:', error);
        resultDiv.innerHTML = `<p class="error">Failed to fetch price. ${error.message}. Check console for details.</p>`;
    }
}
