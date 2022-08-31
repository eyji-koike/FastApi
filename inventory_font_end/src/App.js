import {Products} from "./components/Products";
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {Create_Products} from "./components/Create_Products";

function App() {
    return <BrowserRouter>
        <Routes>
            <Route path="/" element={<Products/>}/>
            <Route path="/create" element={<Create_Products/>}/>
        </Routes>
    </BrowserRouter>;
}

export default App;