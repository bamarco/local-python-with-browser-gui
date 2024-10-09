<template>
    <div :style="{'display': 'flex',
                  'flex-direction': 'column'}">
        <h1>Ping Pong</h1>
        <button @click="pingServer">Ping</button>
        <code>
            {{ ball }}
        </code>
    </div>
</template>
<script setup>
import { ref } from "vue";
const ball = ref("");

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function last(arr) {
  return arr[arr.length - 1];
}

function serverPort() {
     let port = last(window.location.origin.split(":"));
     if ("5173" == port) {
         // When using the default vite development port for the frontend 5173,
         // also use flask default backend server port 5000
         port = "5000";
     }
     return port;
}

async function pingServer() {
     ball.value = "pinging...";
     let port = serverPort();
     await fetch(`http://127.0.0.1:${port}/ping`)
        .then(async (response) => {
            const payload = await response.json();
            await sleep(500);
            ball.value = payload.msg;
            return payload;
        })
        .catch((err) => {
            console.log(err);
            return err;
        } );
}
</script>
