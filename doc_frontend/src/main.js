import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'world',
        title: 'svete',
	}
});

export default app;
