import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
        title: 'Semantic document storage',
        doc_api: ''
	}
});

export default app;
