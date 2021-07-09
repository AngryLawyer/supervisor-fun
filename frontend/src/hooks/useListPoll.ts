import { useRef, useEffect, useState } from 'react';
import { Message } from '../types';

export const useListPoll = () => {
  const intervalRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const [state, setState] = useState<readonly Message[]>([]);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      fetch('/list')
        .then((response) => response.json())
        .then(setState);
    }, 1000);
    return () => {
      clearInterval(intervalRef.current!);
    };
  }, [setState]);

  return state;
}
