const primitiveToComponent = {
  orientation: (block) => ({
    type: "Body",
    props: {
      text: block.content.text,
      role: "intro"
    }
  }),

  subhead: (block) => ({
    type: "Heading",
    props: {
      level: 2,
      text: block.content.text
    }
  }),

  definition: (block) => ({
    type: "Body",
    props: {
      text: `${block.content.term}: ${block.content.meaning}`
    }
  }),

  impact_statement: (block) => ({
    type: "Body",
    props: {
      text: block.content.text,
      emphasis: "high"
    }
  }),

  knowledge_check: (block) => ({
    type: "MCQ",
    props: block.content
  })
};
