import { useEffect } from 'react'
import { sessionState, useChatSession } from "@chainlit/react-client";
import { Playground } from '@/page/playground'
import { useRecoilValue } from "recoil";

import './App.css'

function App() {
  const { connect } = useChatSession();
  const session = useRecoilValue(sessionState);
  
  const userEnv = {}
  useEffect(() => {
    if (session?.socket.connected) {
      return;
    }
    fetch("http://localhost:80/custom-auth", {
      headers: {
        "Content-Type": "application/json",
      }
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        connect({
          userEnv,
          accessToken: `Bearer: ${data.token}`,
        });
      });
  }, [connect]);

  return (
    <>
      <Playground/>
    </>
  )
}

export default App
