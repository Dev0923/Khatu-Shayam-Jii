import { RouterProvider } from "react-router";
import { router } from "./routes";
import { AlertListener } from "./components/AlertListener";

export default function App() {
  return (
    <>
      <RouterProvider router={router} />
      <AlertListener />
    </>
  );
}
