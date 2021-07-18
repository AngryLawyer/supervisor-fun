import { useCallback } from "react";
import { Action } from "../types";

export const useSendMessage = () => {
  return useCallback((id: string, action: Action) => {
    return fetch(`/${id}/action`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: action.id,
      }),
    });
  }, []);
};
