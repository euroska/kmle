<svelte:head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</svelte:head>

<script>
    import { Button, Input, FormGroup, Container, Row, Col } from 'sveltestrap';
    import { onMount } from "svelte";
    import { formatDate } from 'timeUtils'
    export let title;
    export let doc_api;

    const bg = ["bg-light", "bg-white", "bg-warning", "bg-warning"];

    document.title = title;

    let documentList = [];

    onMount(async () => {
        const response = await fetch(
            `${doc_api}/v1/document/`,
            { method: 'get', mode: "cors" }
        );
        const documentListResponse = await response.json();
        let newDocumentList = documentList;

        for(let document of documentListResponse) {
            document.meta.timeOfCreation = new Date(document.meta.timeOfCreation);
            document.new = 0;
            newDocumentList.push(document);
        }
        documentList = newDocumentList;
    });

    function handleUpload() {
        const input = document.querySelector('input[type="file"]')
        let newDocumentList = documentList;
        for(let file of input.files) {
            let data = new FormData()
            data.append('document', file)
            fetch(`${doc_api}/v1/document/`, {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(data => {
                data.meta.timeOfCreation = new Date(data.meta.timeOfCreation);
                data.new = 2;
                newDocumentList.push(data);
                documentList = newDocumentList;
            });
        }
    }
</script>

<main>
    <h1>{title} !</h1>
    <Container>
        <Row class="text-light bg-dark">
            <Col xs="4">Filename</Col>
            <Col xs="2">Creation</Col>
            <Col xs="2">Creator</Col>
            <Col xs="2">WordCount</Col>
            <Col xs="2">Language</Col>
        </Row>

        {#if documentList}
            {#each documentList as document, i}
                <Row class="{bg[i%2 + document.new]}">
                    <Col xs="4"><a href="{doc_api}/v1/document/{document.uuid}">{document.name}</a></Col>
                    <Col xs="2">{formatDate(document.meta.timeOfCreation, '#{Y}/#{m}/#{d}')}</Col>
                    <Col xs="2">{document.meta.creator}</Col>
                    <Col xs="2">{document.meta.wordCount}</Col>
                    <Col xs="2">{document.meta.language}</Col>
                </Row>
            {/each}
        {:else}
            <Row>
                <Col xs="12">Waiting</Col>
            </Row>
        {/if}
    </Container>
    <hr />
    <FormGroup>
        <Container>
            <Row>
                <Col class="col-6">
                    <Input type="file" name="document" multiple />
                </Col>
                <Col class="col-6">
                    <Button primary class="col-6" on:click={handleUpload}>Upload</Button>
                </Col>
            </Row>
        </Container>
    </FormGroup>
</main>
