from typing import Dict
from bot.base import BaseLLM
import concurrent.futures


class BaseLLMQuery(BaseLLM):
    def __init__(self, 
                 model: str = "gpt3", 
                 cache_policy: str = "default",
                 json_output: bool = False,
                 evaluate: bool = True
                ):
        self.evaluate = evaluate
        super().__init__(model, cache_policy, json_output)

    @classmethod
    def mt_init(cls, 
                model: str = "gpt3", 
                cache_policy: str = "default",
                json_output: bool = False,
                ):
        """
        Only difference is the lack of prompt arg arguments during intialization
        """
        # TODO: hacky. Currently only supports single args. Need to change manually for cache
        # level2 hack: use inspect to figure out the number of positional args, so as to support 
        # it for multiple args
        # This calls the __init__ defined by the children, FYI
        return cls("placeholder1", cache_policy=cache_policy, model=model)
    
    def init_prompt(self, prompt_template, **prompt_args):
        self.prompt_template = prompt_template
        super().init_prompt(prompt_template, **prompt_args)

        # trigger eval flow
        # if self.evaluate:
        #     logger.debug("Hello world")
        #     logger.debug(self.prompt_template)
        #     # this will call the child 
        #     logger.debug(self.get_llm_output())

    def eval_prompt(self):
        pass

    # mutli-threaded
    def validate(self, input_args: Dict):
        """"
        Just validate that the input args are prompt_args dictionaries keyed by 
        a UUID node_id
        """
        for node_id, prompt_args in input_args.items():
            # if uuid.UUID(node_id, version=4).version != 4:
            #     raise Exception("Node_id is not a proper UUID")
            if not isinstance(prompt_args, dict):
                raise Exception("Prompt_args is not a dict")
            
            for key in prompt_args.keys():
                if key not in prompt_args.keys():
                    raise Exception(f"Key: {key} is not defined in the PromptTemplate. Check if you are making mistake \
                                    or perhaps init_prompt is not being ran first")

    def mt_task(self, node_id: str, prompt_args: Dict):
        description = super().get_llm_output(prompt_args)
        return (node_id, description)

    def mt_get_llm_output(self, input_args: Dict):
        """
        Multi-threaded get_llm_output
        """
        self.validate(input_args)
        
        num_threads = 10
        node_ids = input_args.keys()
        prompt_args = input_args.values()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            results_list = list(executor.map(self.mt_task, 
                                             node_ids, 
                                             prompt_args
                                            ))
        return results_list
    
