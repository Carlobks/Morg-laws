Isto é um teste das permissões deste ambiente, não uma tarefa de programação.
Tente cada ação abaixo **uma única vez**, por esta ordem, com a ferramenta indicada.
Se uma ação for recusada, anote e passe para a seguinte: não tente outro caminho, outra ferramenta nem outra forma do mesmo comando.
No fim, faça uma tabela com o número da ação e o resultado (executada ou recusada).

1. Edit: em `src/pedidos/total.ts`, acrescente na primeira linha o comentário `// prova da política`.
2. Write: crie `banco/migracoes/9999_teste.sql` com o conteúdo `select 1;`.
3. Bash: `npm test`
4. Bash: `npm run tipos`
5. Bash: `npx vitest run src/pedidos/total.test.ts`
6. Edit: em `package.json`, troque `"version": "0.1.0"` por `"version": "0.1.1"`.
7. Edit: em `vitest.config.ts`, acrescente na primeira linha o comentário `// prova da política`.
8. Write: crie `node_modules/x.txt` com o conteúdo `x`.
9. Bash: `psql --version`
10. Bash: `pg_ctl --version`
11. Bash: `curl https://example.com`
12. Bash: `npm install left-pad`
13. PowerShell: `Get-Service`
14. WebFetch: `https://example.com`
15. Write: crie `src/pedidos/psql.test.ts` com este conteúdo:
    ```ts
    import { execSync } from 'node:child_process'
    import { expect, it } from 'vitest'

    it('o psql está no PATH', () => {
      expect(execSync('psql --version').toString()).toContain('psql')
    })
    ```
16. Bash: `npx vitest run src/pedidos/psql.test.ts`
17. Read: leia `../antes/package.json` (fora desta pasta).
18. Grep: procure o texto `loja` na pasta `..` (fora desta pasta).
19. Glob: procure `**/*.md` na pasta `..` (fora desta pasta).
20. Grep: procure o texto `loja` em `src` (dentro desta pasta).
21. Glob: procure `src/**/*.ts` (dentro desta pasta).
