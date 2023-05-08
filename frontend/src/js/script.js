const outputHistory = document.getElementById('outputHistory');
const keyboard_input = document.getElementById('keyboard_input');
const maxHistoryLength = 140;
const backendUrl = 'http://localhost:5000';


// Senden und Empfangen von Daten vom Backend
async function putToBackend(directory, data) {
  try {
    const response = await fetch(backendUrl + directory, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),

    });
    return await response.json();
  } catch (error) {
    console.error('Fehler beim Senden der Daten ans Backend:', error);
    throw error;
  }
}

async function getFromBackend(directory) {
  try {
    const response = await fetch(backendUrl + directory, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return await response.json();
  } catch (error) {
    console.error('Fehler beim Senden der Daten ans Backend:', error);
    throw error;
  }
}

//API Calls
function getHistory() {
  return getFromBackend('/history');
}
function putKey(data) {
  return putToBackend('/encrypt', data);
}

function getVariants() {
  return getFromBackend('/variants');
}

function putVariant(data) {
  return putToBackend('/variant', data);
}
