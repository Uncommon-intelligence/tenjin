import { Worker, Viewer } from "@react-pdf-viewer/core";
import { highlightPlugin, Trigger } from "@react-pdf-viewer/highlight";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

// type Zoom = (scale: number | SpecialZoomLevel) => void;

const PDFViewer = ({ pdfURL }: { pdfURL: string }) => {
    const defaultLayoutPluginInstance = defaultLayoutPlugin();
    const highlightPluginInstance = highlightPlugin({
        trigger: Trigger.None,
    });

    return (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.3.122/build/pdf.worker.min.js">
            <Viewer
                plugins={[defaultLayoutPluginInstance, highlightPluginInstance]}
                fileUrl="/example.pdf"
            />
        </Worker>
    );
};

export default PDFViewer;
