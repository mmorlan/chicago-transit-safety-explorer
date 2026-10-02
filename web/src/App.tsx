import { AppHeader } from "./components/AppHeader";
import { StationMap } from "./components/StationMap";

export default function App() {
  return (
    <div className="app">
      <AppHeader />
      <main className="app-main">
        <StationMap />
      </main>
    </div>
  );
}
