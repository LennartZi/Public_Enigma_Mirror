const outputHistory = document.getElementById('outputHistory');
const keyboard_input = document.getElementById('keyboard_input');
const maxHistoryLength = 140;
const backendUrl = 'http://localhost:5000';

const rows = [
  'qwertyuiop',
  'asdfghjkl',
  'zxcvbnm'
];

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

// Erstellen der Tasten
function createKeys(keyboardDiv) {
  for (let rowIndex = 0; rowIndex < rows.length; rowIndex++) {
    const row = document.createElement('div');
    row.classList.add('row');
    const keys = rows[rowIndex];

    for (let i = 0; i < keys.length; i++) {
      const key = document.createElement('div');
      key.classList.add('key_input');
      key.textContent = keys[i].toUpperCase();

      row.appendChild(key);
    }

    keyboardDiv.appendChild(row);
  }
}

createKeys(keyboard_input);

