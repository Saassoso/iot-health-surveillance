import { initializeApp } from "firebase/app";
import { getDatabase, ref, onValue } from "firebase/database";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {

  apiKey: "AIzaSyC0zR0JUzB7mAt9YwM1B7wL7mP9g3GWJdM",

  authDomain: "node-red-io.firebaseapp.com",

  databaseURL: "https://node-red-io-default-rtdb.europe-west1.firebasedatabase.app",

  projectId: "node-red-io",

  storageBucket: "node-red-io.firebasestorage.app",

  messagingSenderId: "515414424029",

  appId: "1:515414424029:web:4d20a9d0b81e770e95de34"

};


const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const analytics = getAnalytics(app);

export { database, ref, onValue };

